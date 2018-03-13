#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
char *code;
unsigned char *ptr; 
unsigned char *op; 
unsigned char *tp;
int flag=0; 
int mess=3;
char p1[8]="63211234";
char n1[8]="Alice";
char p2[8]="63204321";
char n2[8]="Bob";
char p3[8]="63121290";
char n3[8]="Dave";
char shellcode[120]="\x68\x6f\x64\x20\x01\x81\x34\x24\x01\x01\x01\x01\x48\xb8\x75\x79\x20\x61\x20\x70\x68\x6f\x50\x48\xb8\x61\x6e\x20\x6e\x6f\x74\x20\x62\x50\x48\xb8\x65\x72\x2c\x79\x6f\x75\x20\x63\x50\x48\xb8\x42\x61\x64\x20\x68\x61\x63\x6b\x50\x6a\x01\x58\x6a\x01\x5f\x6a\x23\x5a\x48\x89\xe6\x0f\x05\xc9\xc3";

typedef struct b{
	unsigned char pass[100];
	char *optr;
	char opcode[2000];
}b; 
b BSS={"0",0,"hhhhhhhhhhhhhhhhh[ur]N{1m}ooooooooooooooooorrrrr[ur]N{1m}haaaa[au]N{1m}hrrr[ur]N{1m}haaa[au]N{1m}hrrraar[ur]N{1m}haaaarr[au]N{1m}hr[ur]N{1m}haa[au]N{1m}hrar[ur]N{1m}haaraa[au]N{1m}haa[ur]N{1m}haarr[au]N{1m}hrarr[ur]N{1m}haarar[au]N{1m}hraar[ur]N{1m}ha[au]N{1m}hrrr[ur]N{1m}haa[au]N{1m}\x00"
				
};
void bf(char *cmd){
while(cmd[flag]){
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
default :puts("error");exit(0);
}
}
}
int checkpass(){
	puts("password:");
	*op=0;
	*tp=0;
	fgets(BSS.pass,2000,stdin);
	ptr=BSS.optr;
	bf(BSS.opcode);
	flag=0;
 int des[]={134,19, 129, 9, 98, 255, 68, 211, 63, 205, 25, 176, 251, 136, 253, 174, 32, 223};
for(int i=0;i<18;i++){
	if(des[i]!=BSS.pass[i]) {return 0;}
	 
}
return 1;
}
void init(){
   op=(int *)malloc(sizeof(int));
   tp=(int *)malloc(sizeof(int));
	srand(time(0));
	code=mmap((0x10000+rand()*0x1000)%0xffffffff,0x1000,7,50,-1,0);
	strcpy(code,shellcode);
	BSS.optr=BSS.pass;
	setbuf(stdin,0);
	setbuf(stdout,0);
    setbuf(stderr,0);
}
void logout(){
	puts("Homura Beeper,plz login!");
	if(!checkpass()){puts("wrong password!\nExit....");exit(0);}
	else return ;
	}
typedef struct mail{
	char *context;
	char *name;
}mail;
typedef struct func{
	char *a;
	int **bb;
}func;
void beeper(mail **m){
	strcpy(m[0]->context,p1);
	strcpy(m[0]->name,n1);
	strcpy(m[1]->context,p2);
	strcpy(m[1]->name,n2);
	strcpy(m[2]->context,p3);
	strcpy(m[2]->name,n3);
	
}
int menu(){
	puts("1.Show the message.");
	puts("2.Remove the message.");
	puts("3.Buy a cell phone.");
	puts("4.Logout.");
	printf("choice>>");
	int x;
	scanf("%d",&x);
	getchar();
	return x;
}
void show(mail **m){
	printf("There are %d messages, number:",mess);
	int c;	
	scanf("%d",&c);
	getchar();
	if(c<0||c>2) {puts("invalid");return ;}
	else{
	printf("%s called you,phone number:",m[c]->name);
	write(1,m[c]->context,8);
	puts("\n");

}
}
void rem(mail **m){
	if(!mess){puts("No message!");return ;}
	else{
	printf("which to remove?");
	int c;
	scanf("%d",&c);
	getchar();
	if(c<0||c>2) {puts("invalid");return ;}
	else{free(m[c]);}
	mess--;
}
}
void buy(int *p){
	(*(void(*)(void))p)();
	return ;
}
int main(){
	init();
	puts("Homura Beeper,plz login!");
	char x[10];

	while(!checkpass()){puts("wrong password!");}
	puts("welcome!");
	mail *m[3];
	m[0] = (mail *)malloc(sizeof(mail));
	m[0]->context=(char *)malloc(20);
	m[0]->name = (char *)malloc(20);
	m[1] = (mail *)malloc(sizeof(mail));
	m[1]->context=(char *)malloc(20);
	m[1]->name=(char *)malloc(20);
	func *d = (func *)malloc(sizeof(mail));
	d->a=(char *)malloc(20);
	d->bb=malloc(20);
	m[2] = (mail *)malloc(sizeof(mail));
	m[2]->context=(char *)malloc(20);
	m[2]->name=(char *)malloc(20);
	beeper(m);
	d->bb[2]=code;
	while(1){
		switch(menu()){
		case 1:show(m);break;		
		case 2:rem(m);break;
		case 3:buy(d->bb[2]);puts("\n");break;
		case 4:logout();break;
		default:puts("invalid");break;
		}
    }
return 0;	
}

