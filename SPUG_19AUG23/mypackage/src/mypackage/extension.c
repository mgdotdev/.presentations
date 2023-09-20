#include <Python.h>
#include <stdio.h>

static PyObject* hello_world(PyObject* self) {
    puts("hello world!");
    Py_RETURN_NONE;
}

static PyMethodDef MethodTable[] = {
    {"hello_world", (PyCFunction)hello_world, METH_NOARGS, "prints 'hello world!' from C"},
    {NULL,}
};

static PyModuleDef Extension = {
    PyModuleDef_HEAD_INIT,
    .m_name = "hello_world",
    .m_doc = "the hello_world module",
    .m_size = -1,
    .m_methods = MethodTable,
};

PyMODINIT_FUNC PyInit_hello_world() {
    return PyModule_Create(&Extension);
}
