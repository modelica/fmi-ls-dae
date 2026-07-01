#ifndef config_h
#define config_h
#include <stdbool.h> // for bool

// define class name and unique id
#define MODEL_IDENTIFIER SimpleDAE
#define INSTANTIATION_TOKEN "{BD403596-3166-4232-ABC2-DAE}"

#define MODEL_EXCHANGE

#define MAX_CONTINUOUS_STATES 2

#define SET_FLOAT64
#define GET_BOOLEAN
#define SET_BOOLEAN
#define GET_PARTIAL_DERIVATIVE

#define FIXED_SOLVER_STEP 1e-2
#define DEFAULT_STOP_TIME 20

typedef enum {
    vr_time, vr_x1, vr_der_x1, vr_x2, vr_der_x2, vr_z1,
    vr_z2, vr_u1, vr_u2, vr_y1, vr_y2, vr_res1, vr_res2,
    vr_ode_dae
} ValueReference;

typedef struct {
    double x1;
    double der_x1;
    double x2;
    double der_x2;
    double z1;
    double z2;
    double u1;
    double u2;
    double y1;
    double y2;
    double res1;
    double res2;
    bool ode_dae;
} ModelData;

#endif /* config_h */
