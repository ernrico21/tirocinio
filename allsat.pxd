cdef extern from "list.h":
    cdef struct list:
        int* value;
        list *next;
cdef extern from "main.h":
    list* main(char* argv)
