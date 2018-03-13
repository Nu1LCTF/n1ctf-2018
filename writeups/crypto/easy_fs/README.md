# easy_fs

This is a crypto & pwn(?) challenge. 

A binary that do RSA encryption with files or custom strings is provided, and you need to reverse the binary to find bugs.

## Intended solution

First, check the file list. A flag......216 byte. Cannot use the root attack.

After some testing and debugging, you may find that the input function has a vulnerability:

```c
  v7 = a3;
  v9 = a2;
  while ( 1 )
  {
    v6 = v7--;
    if ( !v6 )
      break;
    a2 = &v8;
    read(a1, &v8, 1LL);
    if ( v8 == '\n' || v8 == '\xFF' )
    {
      v3 = v9++;
      *v3 = 0;
      return fflush(stdin, &v8);
    }
    v5 = v9++;
    *v5 = v8;
  }
  return fflush(stdin, a2);
```
When you input ```a3``` bytes, it would not add ```\0``` after the string, which can be used to leak informations.

Additionally, when you call ```read_encrypted_file``` function after the ```custom_encryption``` function, the stack frame of the second function will be precisely "on" the former one.

Let's try the information leak......

```
==============================
   Input your choice:         
==============================
2
Input filename:
flag
N = 0x5a418352e89c6e21db3e02c2ca7dfe49d60e07c3ac0bba3ca8adad06a6525315813b8261e1ffb5240247d750190569fc643c10701d9fdc804a2fac7a909d73def23e5e33e3e2c347abfb64ce5a2616caee0c6de116622e0be88609eb030a1710cfde40cb258d24cabe91682c7618c925eab1890c6d09dd29b3c3c31cad935498d92ee07d667364a4c4b8656afe0abe9c5bc6e32c967139921e158ef6ec45ebc8b231219a8d44bbe29ff1a879aa6dbd2a3a18355688125217de9dc0bc4c0d572ba30360bbaef625d706fb36011fedeabcc4db6d6b6d317645b5bf0376668554b1af0fa79a97906013159944c6f213307e603ba60e0f8463212126aa42c0451fb7
Please input your E: (Hexadecimal, without '0x/0X', 1 - 16 digits)
1111111111111111
e = 0x1111111111111111752c0735c30c707861593b62448eb47feede7b9863df226afdeeeb2a464865c087106d80c4a038b9017bebaf8eb70866e5824030756ad6df17bb10a5e38f4b0f8f0ffe8aa9479356fad4b8b712f8a658
Invalid E, use 0x10001
```

Oops. What's that? I think you need the debugger......

Keep tracing the stack frame you will get that the leaked information is just the last ```p```! Length......640 bits. Use ```Coppersmith's Attack``` to get the private key and the flag.

## Flag
```N1CTF{A_sm4ll_l34k_l3ad5_t0_l4rge_br34k}```

## Unintended solution

Some teams use e = 3 to do encryption and get ciphertext, use ```Chinese Remainder Theorem``` to solve the formula.

## BTW

Maybe I had to add constraints on E to prevent the attacks based on low exponents......

The recursion function? It's an original design......Challengers need to call the function recursively to control the stack, in order to get the first 640 bits of ```p``` **right** after ```e```. Should I add this feature? lol
