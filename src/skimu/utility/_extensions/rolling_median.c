#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include "numpy/arrayobject.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include <gsl/gsl_math.h>
#include <gsl/gsl_movstat.h>
#include <gsl/gsl_vector.h>


PyObject * roll_median(PyObject *NPY_UNUSED(self), PyObject *args){
    PyObject *x_;
    long wlen;

    if (!PyArg_ParseTuple(args, "Ol:roll_median", &x_, &wlen)) return NULL;

    PyArrayObject *data = (PyArrayObject *)PyArray_FromAny(
        x_, PyArray_DescrFromType(NPY_DOUBLE), 1, 0,
        NPY_ARRAY_ENSUREARRAY | NPY_ARRAY_CARRAY_RO, NULL
    );
    if (!data) return NULL;

    // get the number of dimensions, and the shape
    int ndim = PyArray_NDIM(data);
    npy_intp *ddims = PyArray_DIMS(data);

    // data pointers
    double *dptr = (double *)PyArray_DATA(data);
    
    gsl_movstat_workspace *w = gsl_movstat_alloc((size_t)wlen);

    gsl_vector x;
    x.size = ddims[ndim-1];
    x.stride = 1;
    // x.data = dptr;  // set this later
    x.block = NULL;
    x.owner = 0;

    // RETURN
    PyArrayObject *rmean = (PyArrayObject *)PyArray_EMPTY(ndim, ddims, NPY_DOUBLE, 0);
    double *rptr = (double *)PyArray_DATA(rmean);

    gsl_vector xmean;
    xmean.size = ddims[ndim-1];
    xmean.stride = 1;
    // xmean.data = rptr;  // set this later
    xmean.block = NULL;
    xmean.owner = 0;

    // for iterating over the data
    long stride = ddims[ndim - 1];
    int nrepeats = PyArray_SIZE(data) / stride;

    for (int i = 0; i < nrepeats; ++i){
        x.data = dptr;
        xmean.data = rptr;

        gsl_movstat_median(GSL_MOVSTAT_END_PADZERO, &x, &xmean, w);

        dptr += stride;
        rptr += stride;
    }
    
    Py_XDECREF(data);

    return (PyObject *)rmean;
}

static struct PyMethodDef methods[] = {
    {"roll_median",   roll_median,   1, NULL},  // last is the docstring
    {NULL, NULL, 0, NULL}          /* sentinel */
};

static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "roll_median",
        NULL,
        -1,
        methods,
        NULL,
        NULL,
        NULL,
        NULL
};

/* Initialization function for the module */
PyMODINIT_FUNC PyInit_roll_median(void)
{
    PyObject *m;
    m = PyModule_Create(&moduledef);
    if (m == NULL) {
        return NULL;
    }

    /* Import the array object */
    import_array();

    /* XXXX Add constants here */

    return m;
}