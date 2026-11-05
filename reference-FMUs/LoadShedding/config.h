#ifndef config_h
#define config_h
#include <stdbool.h> // for bool

// define class name and unique id
#define MODEL_IDENTIFIER LoadShedding
#define INSTANTIATION_TOKEN "{6F2C8E41-7D3A-4B95-A1E6-0C9D5B7F3A28}"

#define MODEL_EXCHANGE

#define MAX_CONTINUOUS_STATES 1
#define MAX_EVENT_INDICATORS 2

#define SET_FLOAT64
#define GET_BOOLEAN
#define SET_BOOLEAN
#define EVENT_UPDATE

#define FIXED_SOLVER_STEP 1e-3
#define DEFAULT_STOP_TIME 2

typedef enum {
    vr_time, vr_v, vr_der_v, vr_i, vr_C, vr_R, vr_RShed, vr_RAux,
    vr_vShed, vr_iMax, vr_res1, vr_g1, vr_g2, vr_shed, vr_tripped,
    vr_ode_dae
} ValueReference;

typedef struct {
    double v;
    double der_v;
    double i;
    double C;
    double R;
    double RShed;
    double RAux;
    double vShed;
    double iMax;
    double res1;
    double g1;
    double g2;
    bool shed;
    bool tripped;
    bool tripCondition; // condition of the when-equation, its pre() value detects the rising edge
    bool ode_dae;
} ModelData;

#endif /* config_h */
