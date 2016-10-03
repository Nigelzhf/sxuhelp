#include "Python.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <openssl/des.h>

char * Encrypt( char *Key, char *Msg, int size);
char * Decrypt( char *Key, char *Msg, int size);
static PyObject *SpamError;

static PyObject *
Cet_des_cfb64(PyObject *self,PyObject *args)
{
    unsigned char * txt;
    unsigned int length;
    unsigned char * key;
    unsigned int C;
    char * r;
    //char *e;
    int i=0;
    PyObject *result;

    //接受python参数
    if(!PyArg_ParseTuple(args,"s#sI",&txt,&length,&key,&C))
    {   
        return NULL;
    }

    //分配result__buffer
    r = malloc(length);

    //加密和解密
    if(C)
        memcpy(r, Encrypt(key, txt, length), length);
    else
        memcpy(r, Decrypt(key, txt, length), length);

    //e=r;
    //for(;i<length;i++) printf("%02x:", (unsigned char)(*(e+i)));
    
    //保存成python结果
    result = PyBytes_FromStringAndSize(r,length);
    //result = PyUnicode_FromStringAndSize(r,length);

    //释放malloc
    free(r);
    return result;
}

static PyMethodDef SpamMethods[]={
    {"cetdes",Cet_des_cfb64,METH_VARARGS,"cet_des_cfb64"},
    {NULL,NULL,0,NULL}
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "cetdes",
    NULL,
    -1,
    SpamMethods
};
PyMODINIT_FUNC
PyInit_cetdes(void)
{
    PyObject *m;
    m = PyModule_Create(&spammodule);
    if(m==NULL)
        return NULL;
    SpamError = PyErr_NewException("cetdes.error",NULL,NULL);
    Py_INCREF(SpamError);
    PyModule_AddObject(m,"error",SpamError);
    return m;
}

char *
Encrypt( char *Key, char *Msg, int size)
{

	static char*    Res;
	int             n=0;
	DES_cblock      Key2;
	DES_key_schedule schedule;

	Res = ( char * ) malloc( size );

	/* Prepare the key for use with DES_cfb64_encrypt */
	memcpy( Key2, Key,8);
	DES_set_odd_parity( &Key2 );
	DES_set_key_checked( &Key2, &schedule );

	/* Encryption occurs here */
	DES_cfb64_encrypt( ( unsigned char * ) Msg, ( unsigned char * ) Res,
			   size, &schedule, &Key2, &n, DES_ENCRYPT );

	 return (Res);
}


char *
Decrypt( char *Key, char *Msg, int size)
{

	static char*    Res;
	int             n=0;

	DES_cblock      Key2;
	DES_key_schedule schedule;

	Res = ( char * ) malloc( size );

	/* Prepare the key for use with DES_cfb64_encrypt */
	memcpy( Key2, Key,8);
	DES_set_odd_parity( &Key2 );
	DES_set_key_checked( &Key2, &schedule );

	/* Decryption occurs here */
	DES_cfb64_encrypt( ( unsigned char * ) Msg, ( unsigned char * ) Res,
			   size, &schedule, &Key2, &n, DES_DECRYPT );

	return (Res);

}
