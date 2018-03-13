// a buggy code, making for the vulnerablities

#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <gmp.h>
mpz_t p, q, n, e, temp, plaintext, cipher, p1, q1;
unsigned char temp_buf[512];
// gmp_randstate_t state;
void initialize()
{
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);
	mpz_init_set_ui(p, 0);
	mpz_init_set_ui(q, 0);
	mpz_init_set_ui(p1, 0);
	mpz_init_set_ui(q1, 0);
	mpz_init_set_ui(n, 0);
	mpz_init_set_ui(e, 0);
	mpz_init_set_ui(temp, 0);
	chdir("filesystem");
	// int fd = open("/dev/urandom", O_RDONLY);
	// if (fd == -1)
	// {
	// 	puts("Error!");
	// 	exit(-1);
	// }
	// unsigned long int seed_n;
	// read(fd, (char *)&seed_n, sizeof(unsigned long int));
	// close(fd);
	// gmp_randinit_mt(state);
	// gmp_randseed_ui(state, seed_n);
	
	return;
}
void generate_n(unsigned char *buff)
{	
	unsigned char *p_digit=buff, *q_digit=buff+300;
	memset(p_digit, 0, 300);
	memset(q_digit, 0, 300);
	memset(temp_buf, 0, sizeof(temp_buf));
	int fd = open("/dev/urandom", O_RDONLY);
	if (fd == -1)
	{
		puts("Error!");
		exit(-1);
	}
	read(fd, temp_buf, 128);
	for(int i = 0; i < 128; i++)
	{
		snprintf(p_digit + i * 2, 3, "%02x", temp_buf[i]);
	}
	mpz_set_str(p, p_digit, 16);
	mpz_nextprime(p, p);
	memset(temp_buf, 0, sizeof(temp_buf));
	read(fd, temp_buf, 128);
	for(int i = 0; i < 128; i++)
	{
		snprintf(q_digit + i * 2, 3, "%02x", temp_buf[i]);
	}
	mpz_set_str(q, q_digit, 16);
	mpz_nextprime(q, q);
	// mpz_urandomb(temp, state, 1024);
	// mpz_nextprime(p, temp);
	// mpz_mul_ui(temp, temp, 3);
	// mpz_fdiv_q_ui(temp, temp, 2);
	// mpz_nextprime(q, temp);
	mpz_mul(n, p, q);
	close(fd);
}
void read_buf(int fd, void* buf, unsigned int nbytes)
{
	char ch;
	char* p = buf;
	while(nbytes--)
	{
		read(fd, &ch, 1);
		if (ch == '\n' || ch == -1)
		{
			*p++ = '\0';
			fflush(stdin);
			return;
		}
		*p++ = ch;
	}
	fflush(stdin);
	return;
}
// inline void read_e()
// {
// 	mpz_set_ui(e, 0);
// 	char buf[16];
// 	memset(buf, 0, sizeof(buf));
// 	read_buf(0, buf, 16);
// 	mpz_set_str(e, buf, 16);
// 	gmp_printf("e = %Zd\n", e);
// 	return;
// }
int check_relatively_prime()
{
	mpz_sub_ui(p1, p, 1);
	mpz_sub_ui(q1, q, 1);
	mpz_mul(temp, p1, q1);
	mpz_gcd(temp, temp, e);
	if (!mpz_cmp_si(temp, 1))
	{
		return 1;
	}
	return 0;
}
void custom_encryption()
{
	struct {
	char off[24];
	unsigned char buff[160];
	char digital_buf[848];
	}sta;
	puts("Now generating N......");
	
	generate_n(sta.buff);
	gmp_printf("N = 0x%Zx\n", n);
	//gmp_printf("p = 0x%Zx\n", p);
	//gmp_printf("q = 0x%Zx\n", q);
	puts("Please input your E: (Hexadecimal, without '0x/0X', 1 - 16 digits)");
	mpz_set_ui(e, 0);
	char *e_buf=sta.buff-24;
	memset(sta.digital_buf,0,848);
	memset(e_buf, 0, 24);
	read_buf(0, e_buf, 16);
	mpz_set_str(e, e_buf, 16); //(z,str,base)
	gmp_printf("e = 0x%Zx\n", e);
	if(mpz_cmp_si(e, 2) <= 0 || !(check_relatively_prime()))
	{
		puts("Invalid E, use 0x10001");
		mpz_set_str(e, "10001", 16);
	}
	puts("Input your plaintext: (No more than 432 bytes)");
	memset(temp_buf, 0, sizeof(temp_buf));
	read_buf(0, temp_buf, 431);
	for(int i = 0; i < strlen(temp_buf); i++)
	{
		snprintf(sta.digital_buf + i * 2, 3, "%02x", temp_buf[i]);
	}
//	printf("%s\n", digital_buf);
	mpz_set_str(plaintext, sta.digital_buf, 16);
//	gmp_printf("P = 0x%Zx\n", plaintext);
	mpz_powm(cipher, plaintext, e, n);
	puts("Success!");
	gmp_printf("C = 0x%Zx\n", cipher);
	puts("More encryption? (y/n)");
	char c[8];
	read_buf(0, c, 3);
	if (!(strcmp(c, "y")))
	{
		custom_encryption();
	}
	return;
}
void read_encrypted_file()
{
	int fd;
	struct {
		char filename[24];
		char e_buf[16];
		char digital_buf[1024];
	} gg;
	// char filename[24];
	// char e_buf[16];

	puts("Input filename:");
	read_buf(0, gg.filename, 23);
	fd = open(gg.filename, O_RDONLY);
	if (fd == -1)
	{
		puts("Fail opening file!");
		return;
	}
	read(fd, temp_buf, 512);
	//printf("%s",temp_buf);
	close(fd);
	if (mpz_cmp_si(n, 0) == 0)
	{	
		puts("Now generating N......");
		generate_n(gg.digital_buf);
	}
	gmp_printf("N = 0x%Zx\n", n);
	// gmp_printf("p = 0x%Zx\n", p);
	// gmp_printf("q = 0x%Zx\n", q);
	puts("Please input your E: (Hexadecimal, without '0x/0X', 1 - 16 digits)");
	mpz_set_ui(e, 0);
	memset(gg.e_buf, 0, sizeof(gg.e_buf));
	read_buf(0, gg.e_buf, 16);
	mpz_set_str(e, gg.e_buf, 16);
	gmp_printf("e = 0x%Zx\n", e);
	if(mpz_cmp_si(e, 2) <= 0 || !(check_relatively_prime()))
	{
		puts("Invalid E, use 0x10001");
		mpz_set_str(e, "10001", 16);
	}
	for(int i = 0; i < strlen(temp_buf); i++)
	{
		snprintf(gg.digital_buf + i * 2, 3, "%02x", temp_buf[i]);
	}
//	printf("%s\n", digital_buf);
	mpz_set_str(plaintext, gg.digital_buf, 16);
//	gmp_printf("P = 0x%Zx\n", plaintext);
	mpz_powm(cipher, plaintext, e, n);
	puts("Success!");
	gmp_printf("C = 0x%Zx\n", cipher);
	puts("You can just read once :)");
	exit(0);
}
void print_menu()
{
	puts("==============================");
	puts("   Welcome to Nu1L Easy FS    ");
	puts("==============================");
	puts("   1. File list               ");
	puts("   2. Read encrypted file     ");
	puts("   3. Custom encryption       ");
	puts("   4. Quit                    ");
	puts("==============================");
	puts("   Input your choice:         ");
	puts("==============================");
	return;
}
int main()
{
	int choice;
	initialize();
	print_menu();
	scanf("%d", &choice);
	while (choice != 4)
	{
		switch(choice)
		{
			case 1:
				system("ls -l");
				break;
			case 2:
				read_encrypted_file();
				break;
			case 3:
				custom_encryption();
				break;
			default:
				puts("Invalid choice!");
				break;
		}
		print_menu();
		choice = 0;
		scanf("%d", &choice);
	}
	return 0;
}
