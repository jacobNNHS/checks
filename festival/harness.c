// Test harness used by check50 (students never see this file).
// check50 compiles the student's festival.c with -Dmain=student_main so the
// student's main is renamed and this main can call their functions directly.
#undef main
#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int get_int_in_range(int min, int max);
void print_banner(int width, int height);
int next_balance(int balance);
int months_to_goal(int start, int goal);
int total_interest(int start, int goal);
int boxes(int cupcakes, int size);
int remaining(int cupcakes, int size);

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        return 1;
    }
    int a = argc > 2 ? atoi(argv[2]) : 0;
    int b = argc > 3 ? atoi(argv[3]) : 0;

    if (strcmp(argv[1], "range") == 0)
    {
        int n = get_int_in_range(a, b);
        printf("\nRESULT:%i\n", n);
    }
    else if (strcmp(argv[1], "banner") == 0)
    {
        print_banner(a, b);
    }
    else if (strcmp(argv[1], "next") == 0)
    {
        printf("RESULT:%i\n", next_balance(a));
    }
    else if (strcmp(argv[1], "months") == 0)
    {
        printf("RESULT:%i\n", months_to_goal(a, b));
    }
    else if (strcmp(argv[1], "interest") == 0)
    {
        printf("RESULT:%i\n", total_interest(a, b));
    }
    else if (strcmp(argv[1], "boxes") == 0)
    {
        printf("RESULT:%i\n", boxes(a, b));
    }
    else if (strcmp(argv[1], "remaining") == 0)
    {
        printf("RESULT:%i\n", remaining(a, b));
    }
    return 0;
}
