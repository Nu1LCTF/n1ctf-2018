## “beeper” 题解
比赛结束看WP时才发现这题好多都是非预期解，mmap的随机地址，使用time(0)做的种子，的确是可以预测的，但出题人的本意是想让选手 free两个堆块，然后利用未置空的指针，和指向堆上保存随机地址的fd指针来leak的，结果随机地址就这么被算出来了，也就不用逆登录的密码了。
//我应该改一下服务器时间的。。。
本题密码部分的操作，是类似于一个 Brain F**k的解释器，当然也不完全是。

```
switch(cmd[flag]){
case 'h':ptr++;flag++;break;
case 'o':ptr--;flag++;break;
case 'm':(*ptr)++;flag++;break;
case 'u':(*ptr)--;flag++;break;
case 'r':(*op)++;flag++;break;
case 'a':(*op)--;flag++;break;
case 'N':(*tp)=(*op);flag++;break;
case '1':(*tp)--;flag++;break;
case 'L':(*tp)++;flag++;break;
case '[':if(!(*ptr)){while(cmd[flag++]!=']');}else{flag++;}break;
case ']':if(*ptr){while(cmd[--flag]!='[');flag++;}else{flag++;}break;
case '{':if(!(*tp)){while(cmd[flag++]!='}');}else{flag++;}break;
case '}':if(*tp){while(cmd[--flag]!='{');flag++;}else{flag++;}break; 
```
密码的算法其实只是字符之间的相加减而已，看懂了并不难，可能会多解，不过无所谓，进入程序之后，利用remove message功能释放两个堆块后，可以leak出堆上保存的mmap出来的随机地址，得到地址之后，选择退出，退到登录之前，再次输入密码时，可以覆盖密码地址为shellcode地址，覆盖操作码，将shellcode改写为执行 /bin/sh 即可。

## Writeup for “beeper”


At the end of the game, when I saw some team's WriteUps, I fount that many solutions are not intended.
The random address of mmap, using time (0) as the seed, was indeed predictable, but my intention was to make players free two chunks.And then use the non-empty pointer, and the fd pointer to the random address on the heap to leak the random address. But now there is no need to reverse the login password.
//Maybe I should change the server time. . .

The password part of this challenge is similar to a Brain F**k interpreter, and certainly not entirely.

```
switch(cmd[flag]){
case 'h':ptr++;flag++;break;
case 'o':ptr--;flag++;break;
case 'm':(*ptr)++;flag++;break;
case 'u':(*ptr)--;flag++;break;
case 'r':(*op)++;flag++;break;
case 'a':(*op)--;flag++;break;
case 'N':(*tp)=(*op);flag++;break;
case '1':(*tp)--;flag++;break;
case 'L':(*tp)++;flag++;break;
case '[':if(!(*ptr)){while(cmd[flag++]!=']');}else{flag++;}break;
case ']':if(*ptr){while(cmd[--flag]!='[');flag++;}else{flag++;}break;
case '{':if(!(*tp)){while(cmd[flag++]!='}');}else{flag++;}break;
case '}':if(*tp){while(cmd[--flag]!='{');flag++;}else{flag++;}break; 
```
The algorithm of the password is just the addition and subtraction between the characters. It is not difficult if you understand that.
After entering the program, using the remove message function to release two chunks, then you can leak the random address of shellcode.

Select to exit, entering the password again, you can override the password address for the shellcode address, overwrite the opcode, rewriting the shellcode to execute /bin/sh.