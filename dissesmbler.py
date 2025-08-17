import idaapi

static_address = 0x3008
dynamic_address = 0x0000555555557008

vmcode = []
for i in range(0x3b1a): 
    x = idaapi.get_byte(dynamic_address + i)
    #print(hex(x).strip("0x"))
    #vmcode.append(hex(x).strip("0x"))
    vmcode.append(hex(x)[2:])

print(vmcode)

diss_vm = open("diss_vm.txt", "w")

def fetch_4bytes(start):
    val = 0x00
    for j in range(4):
        val = val | ((int(vmcode[start + j], 16) << 8 * j))
    return val

#       R0   R1    R2    R3
reg = [0x00, 0x00, 0x00, 0x00]
reg2 = [0x00, 0x00, 0x00, 0x00]
i = 0
#dicto = {0x1 : "12345678"}

rbx = ["78", "4e", "56", "61", "32", "5f", "4e", "30", "37"]

while i < len(vmcode):
    if vmcode[i] == "f6": 
        print("EXECUTING => ", vmcode[i])
        eax = int(vmcode[i + 1], 16)
        #print("sub_OP = ", hex(subop))
        ecx = eax & 3
        #print("ecx = ", ecx)
        if ecx == 2:
            #ecx = 0x00
            #for j in range(4):
                #ecx = ecx | ((int(vmcode[i + 2 + j], 16) << 8 * j))
                #print("ECX = ", hex(ecx))
            ecx = fetch_4bytes(i + 2)
            #print(hex(ecx))
            eax = (eax >> 4) & 3
            i = i + 6
            reg[eax] = ecx
            #print(f"reg [{eax}] = {hex(reg[eax])}")
            diss_vm.write(f"mov reg{eax}, {hex(reg[eax])} \n")     
            # break
        elif ecx == 0:
            # swap the values of 2 regiters
            ecx = eax
            eax = (eax >> 4) & 3
            i = i + 5
            ecx = (ecx >> 6) & 3      
            # diss_vm.write(f"mov ecx, reg{ecx} \n")
            ecx = reg[ecx]
            diss_vm.write(f"mov reg{eax}, {hex(ecx)} \n")
            reg[eax] = ecx
        else:
            i = i + 1
        print("next => ", vmcode[i])
        continue 


    elif vmcode[i] == "aa":
        print("EXECUTING => ", vmcode[i])
        eax = int(vmcode[i + 1] , 16)
        ecx = eax & 3
        if ecx == 2:
            eax = (eax >> 4) & 3
            i = i + 8
            ecx = reg[eax]         
            ecx = ecx - fetch_4bytes(i - 6)
            diss_vm.write(f"sub reg{eax}, {hex(ecx)} \n")          
            reg[eax] = ecx
            # print(f"reg [{eax}] = {hex(reg[eax])} \n")
        elif ecx == 0:
            ecx = eax
            eax = (eax >> 6) & 3
            i = i + 3
            ecx = (ecx >> 4) & 3
            esi = reg[ecx]
            diss_vm.write(f"sub reg{ecx}, reg{eax} \n")
            esi = esi - reg[eax]
            reg[ecx] = esi
        else: 
            i = i + 1
        print("next => ", vmcode[i])
        continue
            
        
    elif vmcode[i] == "ef":
        print("EXECUTING => ", vmcode[i])
        eax = int(vmcode[i + 1], 16)
        ecx = eax & 3
        print("ecx = ", ecx)
        vm_ip = i + 2
        if ecx == 0: 
            edx = eax
            eax = (eax >> 4) & 3
            edx = edx >> 6
            fd = reg[eax]
            buff = reg[edx]
            n = 1
            diss_vm.write(f"write({fd}, {hex(buff)}, {n}) \n")
            # Note i = i + 9? 
            i = vm_ip
        elif ecx == 1: 
            eax = (eax >> 6) 
            fd = int(vmcode[i + 2], 16)
            n = 1
            buff = reg[eax]
            diss_vm.write(f"write({fd}, {hex(buff)}, {n}) \n")
            i = vm_ip + 2
        elif ecx == 2:
            eax = (eax >> 4) & 3
            n = 1
            fd = reg[eax]
            buff = int(vmcode[i + 2], 16)
            diss_vm.write(f"write({fd}, {hex(buff)}, n) \n")
            i = vm_ip + 1
        elif ecx == 3:
            fd = int(vmcode[i + 3], 16)
            buff = int(vmcode[i + 2], 16)
            n = 1
            diss_vm.write(f"write({fd}, {hex(buff)}, n) \n")
            i = vm_ip + 3
        else:
            i = i + 1 
        print("next => ", vmcode[i])
        continue


    elif vmcode[i] == "4a":
        vm_ip = i + 2
        eax = int(vmcode[i + 1], 16)
        esi = eax & 3

        if esi == 2:   
            #print("case 2")
            eax = (eax >> 4) & 3
            ecx = fetch_4bytes(i + 2)
            i = i + 7
            diss_vm.write(f"mov reg{eax}, {hex(ecx)}\n")
            reg[eax] = ecx
        elif esi == 0:
            edx = eax 
            eax = (eax >> 6) & 3
            edx = (edx >> 4) & 3
            eax = reg[eax]
            diss_vm.write(f"add reg{edx}, {hex(eax)}\n")
            reg[edx] = reg[edx] + eax
            i = vm_ip
        else:
            i = i + 1
        print("next => ", vmcode[i])
         
        continue



    elif vmcode[i] == "8b":
        vm_ip = i + 2
        eax = int(vmcode[i + 1], 16)
        ecx = eax & 3
        if ecx == 2:
            eax = (eax >> 4) & 3
            i = i + 6
            ecx = reg[eax]
            diss_vm.write(f"xor reg{eax}, {hex(fetch_4bytes(i - 4))}\n")
            ecx = ecx ^ fetch_4bytes(i - 4)
            reg[eax] = ecx
        elif ecx == 0:
            ecx = eax
            eax = (eax >> 6) & 3
            i = i + 3 
            ecx = (ecx >> 4) & 3
            eax = reg[eax]
            diss_vm.write(f"xor reg{ecx}, reg{eax} \n")
            reg[ecx] = reg[ecx] ^ eax
        else:
            i = i + 1
        print("next => ", vmcode[i])
        continue
    
    elif vmcode[i] == "5d":
        print("EXEC = ", vmcode[i])
        vm_ip = i + 2
        eax = int(vmcode[i + 1], 16)
        ecx = eax & 3
        print("ECX = ", ecx)
        if ecx == 2:
            ebp = i + 2
            i = i + 8
            eax = (eax >> 4) & 3
            fd = 0
            n = ebp
            buff = eax
            diss_vm.write(f"read({fd}, &reg{eax}, n) \n")
        elif ecx == 0: 
            ecx = eax
            i = i + 3
            ecx = (ecx >> 6) & 3
            vm_ip = i
            ebp = reg[ecx]
            eax = (eax >> 4) & 3
            fd = 0
            n = ebp
            buff = eax
            diss_vm.write(f"read({fd}, &reg{eax}, reg{ecx}) \n")
            
        else: 
            i = i + 1 
        print("next => ", vmcode[i])
        
        continue


    elif vmcode[i] == "7c":
        vm_ip = i + 2
        eax = int(vmcode[i + 1], 16)
        ecx = eax & 3

        if ecx == 0:
            esi = eax
            eax = (eax >> 6) & 3
            i = i + 4
            esi = (esi >> 4) & 3
            ecx = reg[eax]
            diss_vm.write(f"shl reg{esi}, {hex(ecx)} \n")
            reg[esi] = reg[esi] << ecx
        elif ecx == 2:
            eax = (eax >> 4) & 3
            ecx = int(vmcode[i + 2], 16)
            i = i + 7
            diss_vm.write(f"shl reg{eax}, {hex(ecx)} \n")
            reg[eax] = (reg[eax] << ecx)
        else:
            i = i + 1
        
        continue
        
    elif vmcode[i] == "b1":
        vm_ip = i + 2
        eax = int(vmcode[i + 1], 16)
        ecx = eax & 3

        if ecx == 0: 
            edx = eax
            eax = (eax >> 6) & 3
            edx = (edx >> 4) & 3
            ecx = reg[eax]
            diss_vm.write(f"shr reg{edx}, {hex(ecx)} \n")            
            reg[edx] = reg[edx] >> ecx
            # i = i + 3 ? 
            i = vm_ip
        elif ecx == 2: 
            eax = (eax >> 4) & 3
            ecx = int(vmcode[i + 2], 16)
            i = i + 6
            diss_vm.write(f"shr reg{eax}, {hex(ecx)} \n")            
            reg[eax] = reg[eax] >> ecx
        else:
            i = i + 1
        continue

    elif vmcode[i] == "d5":
        vm_ip = i + 2
        eax = int(vmcode[i + 1], 16)
        ecx = eax & 3
        
        if ecx == 2:
            eax = fetch_4bytes(i + 2)
            eax = ((~eax) & 7) + 1
            diss_vm.write(f"rol {hex(eax)} \n")
            i = i + 5
        elif ecx == 3:
            eax = fetch_4bytes(i + 2)
            eax = ((~eax) & 7) + 1
            diss_vm.write(f"ror {hex(eax)} \n")
            i = i + 9
        elif ecx == 1:
            i = i + 3
        else:
            i = i + 4

        
        continue
    elif vmcode[i] == "1e":
        vm_ip = i + 2
        eax = int(vmcode[i + 1], 16)
        eax = eax & 3
        diss_vm.write("swap registers reg and reg2 \n")
        if eax == 3:
            i = i + 10
        elif eax == 2:
            i = i + 9
        elif eax == 1:
            i = i + 8
        else:
            ecx = i + 3
            i = i + 8
            if eax != 1:
                i = ecx
            eax = i + 1
            vm_ip = i
            eax = int(vmcode[i], 16)
            if eax == 0xaa:
                print("EXECUTING => ", vmcode[i])
                eax = int(vmcode[i + 1] , 16)
                ecx = eax & 3
                if ecx == 2:
                    eax = (eax >> 4) & 3
                    i = i + 8
                    ecx = reg[eax]         
                    diss_vm.write(f"mov ecx, reg{eax} \n")
                    diss_vm.write(f"sub ecx,{hex(fetch_4bytes(i - 6))} \n")
                    ecx = ecx - fetch_4bytes(i - 6)
                    diss_vm.write(f"mov reg{eax}, ecx \n")
                    reg[eax] = ecx
                    # print(f"reg [{eax}] = {hex(reg[eax])} \n")
                elif ecx == 0:
                    ecx = eax
                    eax = (eax >> 6) & 3
                    i = i + 3
                    ecx = (ecx >> 4) & 3
                    diss_vm.write(f"mov esi, reg{ecx} \n")
                    esi = reg[ecx]
                    diss_vm.write(f"sub esi, reg{eax} \n")
                    esi = esi - reg[eax]
                    diss_vm.write(f"mov reg{ecx}, esi \n")
                    reg[ecx] = esi
                else: 
                    i = i + 1
                print("next => ", vmcode[i])
            else:
                print("EXECUTING => ", vmcode[i])
                eax = int(vmcode[i + 1], 16)
                ecx = eax & 3
                if ecx == 2:
                    ecx = fetch_4bytes(i + 2)
                    eax = (eax >> 4) & 3
                    i = i + 6
                    reg[eax] = ecx
                    diss_vm.write(f"mov reg{eax}, {hex(reg[eax])} \n")     
                    # break
                elif ecx == 0:
                    # swap the values of 2 regiters
                    ecx = eax
                    eax = (eax >> 4) & 3
                    i = i + 5
                    ecx = (ecx >> 6) & 3      
                    # diss_vm.write(f"mov ecx, reg{ecx} \n")
                    ecx = reg[ecx]
                    diss_vm.write(f"mov reg{eax}, {hex(ecx)} \n")
                    reg[eax] = ecx
                else:
                    i = i + 1
                print("next => ", vmcode[i])
        continue
    elif vmcode[i] == "c3":
        eax =  int(vmcode[i + 1], 16)
        ecx = eax & 3
        if ecx == 0:
            ecx = eax
            eax = (eax >> 6) & 3
            ecx = (ecx >> 4) & 3
            eax = reg[eax]
            print("EAX = ", eax)
            diss_vm.write(f"cmp reg{ecx}, {hex(eax)} \n")
            i = i + 4
        elif ecx == 2:
            eax = (eax >> 4) & 3
            edi = fetch_4bytes(i + 2)
            diss_vm.write(f"cmp reg{eax}, {hex(edi)} \n")
            i = i + 7
        else:
            i = i + 1
        continue
    i = i + 1
        

    
# D349 x = D3
# D3 << 2



                           


