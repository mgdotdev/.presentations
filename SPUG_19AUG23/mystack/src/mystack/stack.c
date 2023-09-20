#include <Python.h>
#include "structmember.h"

typedef struct {
    PyObject_HEAD
    size_t length;
    PyObject** _data;
    PyObject* push;
    PyObject* pop;
} Stack;

static PyObject* Stack_Push(Stack* self, PyObject* item) {
    size_t len = self->length + 1;
    self->_data = realloc(self->_data, len*sizeof(PyObject*));
    Py_INCREF(item);
    self->_data[self->length] = item;
    self->length = len;
    Py_RETURN_NONE;
}

static PyObject* Stack_Pop(Stack* self) {
    if (self->length == 0)
        Py_RETURN_NONE;
    long len = self->length - 1;
    PyObject* item = self->_data[len];
    self->_data = realloc(self->_data, len*sizeof(PyObject*));
    self->length = len;
    return item;
}

static PyObject* Stack_New(PyTypeObject* type, PyObject* args, PyObject* kwargs) {
    Stack* self = (Stack*)type->tp_alloc(type, 0);
    if (!self)
        return NULL;
    self->length = 0;
    self->_data = malloc(0);
    return (PyObject*)self;
}

static void Stack_Destruct(Stack* self) {
    for (size_t i = 0; i < self->length; i++)
        Py_DECREF(self->_data[i]);
    free(self->_data);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyMemberDef StackMembers[] = {
    {"length", T_LONG, offsetof(Stack, length), READONLY, "stack length"},
    {NULL, }
};

static PyMethodDef StackMethods[] = {
    {"push", (PyCFunction)Stack_Push, METH_O, "push item to the stack"},
    {"pop", (PyCFunction)Stack_Pop, METH_NOARGS, "pop an item to the stack"},
    {NULL, }
};

static PyTypeObject StackType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "stack.Stack",
    .tp_basicsize = sizeof(Stack),
    .tp_dealloc = (destructor)Stack_Destruct,
    .tp_flags = Py_TPFLAGS_DEFAULT|Py_TPFLAGS_BASETYPE,
    .tp_doc = "Stack objects",
    .tp_methods = StackMethods,
    .tp_members = StackMembers,
    .tp_new = Stack_New,
};

static PyModuleDef StackModule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "stack",
    .m_doc = "module for custom stack object",
    .m_size = -1,
    .m_methods = NULL
};

PyMODINIT_FUNC PyInit_stack() {
    if (PyType_Ready(&StackType) < 0)
        return NULL;

    PyObject* module = PyModule_Create(&StackModule);
    if (!module)
        return NULL;

    Py_INCREF(&StackType);
    PyModule_AddObject(module, "Stack", (PyObject*)&StackType);
    return module;
}

