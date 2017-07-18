/* Incoming data parser */

#include <Arduino.h>

void parse(char *command)
{
	/* Allocate */
	char _command[strlen(command) / sizeof(char)];

	/* Tokenization */
	char *delim = " \n";
	char *token;

	strcpy(_command, command);
	while (token = strtok(_command, delim))
	{

	}
}