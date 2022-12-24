SECTION .text

global main

main:
    # input will be a hex value for example (0x12345678)
    mov eax, 0x03
    xor ebx, ebx
    mov edx, 0x4
    lea ecx, DWORD PTR [ebp - 0x4]
    syscall
    # Our input is at the offset ebp - 0x4.
    # Enough Help, Enjoy the algorithm ! 

    mov    eax, DWORD PTR [ebp - 0x4]
    bswap  eax
    mov    edx,eax
    and    eax,0x0f0f0f0f 
    and    edx,0xf0f0f0f0
    shr    edx,0x4
    shl    eax,0x4
    or     eax,edx
    mov    edx,eax
    and    eax,0x33333333
    and    edx,0xcccccccc
    shr    edx,0x2
    shl    eax,0x2
    or     eax,edx
    mov    edx,eax
    and    eax,0x55555555
    and    edx,0xaaaaaaaa
    add    eax,eax
    shr    edx,1
    or     eax,edx
    
    cmp eax, 0xc848b3d5
    je Win 
    jmp Exit

Win: 
    # A function that tells you "Congratulation you can validate with that value !"
    mov eax, 0x04
    xor ebx, ebx
    mov edx, 0x4
    lea ecx, DWORD PTR [ebp - 0x4]
    syscall

Exit: 
    mov eax, 0x01 
    mov ebx, 0x00
    syscall