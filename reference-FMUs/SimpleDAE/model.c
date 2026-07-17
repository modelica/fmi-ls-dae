#include <math.h>

#include "config.h"
#include "model.h"


void setStartValues(ModelInstance *comp) {
    M(x1)     = 0.5;
    M(der_x1) = 0;
    M(x2)     = 0.5;
    M(der_x2) = 0;
    M(z1)     = 0;
    M(z2)     = 0;
    M(u1)     = 0;
    M(u2)     = 0;
    M(y1)     = 0;
    M(y2)     = 0;
    M(res1)   = 0;
    M(res2)   = 0;
}

Status calculateValues(ModelInstance *comp) {
    if (M(ode_dae)) {//DAE
        M(der_x1) = sin(M(x1)) + sin(M(z1) * M(z2) * M(u1));
        M(der_x2) = sin(M(x1) * M(x2)) + sin(M(z1) * M(z2) * M(u2)) + M(u1) * M(u1);
    } else {//ODE
        M(z1)=0;//=h1(u1,u2, x1,x2) to be found analytically or numerically
        M(z2)=0; //=h2(u1,u2, x1,x2) to be found analytically or numerically
        M(der_x1) = sin(M(x1)) + sin(M(z1) * M(z2) * M(u1));
        M(der_x2) = sin(M(x1) * M(x2)) + sin(M(z1) * M(z2) * M(u2)) + M(u1) * M(u1);
    }
    M(res1)   = M(z1) * M(u1) *M(u1) + tanh(3 * M(z1)) + M(u2) * M(x1) * M(x1) * M(x1);
    M(res2)   = exp(M(z1) * M(z2) * M(u1)) / 3 - sin(M(z2) * M(x2));
    M(y1)     = M(u1) * M(x1) * M(z1) + sin(M(u2));
    M(y2)     = M(u2) * M(x2) * M(z2) + sin(M(u1) * M(u2));
    return OK;
}

Status getBoolean(ModelInstance* comp, ValueReference vr, bool values[], size_t nValues, size_t* index) {

    ASSERT_NVALUES(1);
    switch (vr) {
    case vr_ode_dae:    values[(*index)++] = M(ode_dae);   return OK;
    default:
        logError(comp, "GetBoolean is not allowed for value reference %u.", vr);
        return Error;
    }
}

Status setBoolean(ModelInstance* comp, ValueReference vr, const bool values[], size_t nValues, size_t* index) {
    if (comp->state != ConfigurationMode && comp->state != ReconfigurationMode) {
        logError(comp, "Structural variables can only be set in Configuration Mode or Reconfiguration Mode.");
        return Error;
    }

    ASSERT_NVALUES(1);

   switch (vr) {
    case vr_ode_dae: M(ode_dae) = values[(*index)++]; return OK;
    default:
        logError(comp, "SetBoolean is not allowed for value reference %u.", vr);
        return Error;
    }
}
Status getFloat64(ModelInstance* comp, ValueReference vr, double values[], size_t nValues, size_t* index) {

    ASSERT_NVALUES(1);

    calculateValues(comp);

    switch (vr) {
        case vr_time:    values[(*index)++] = comp->time;   return OK;
        case vr_x1:      values[(*index)++] = M(x1);        return OK;
        case vr_der_x1 : values[(*index)++] = M(der_x1);    return OK;
        case vr_x2:      values[(*index)++] = M(x2);        return OK;
        case vr_der_x2:  values[(*index)++] = M(der_x2);    return OK;
        case vr_z1:      values[(*index)++] = M(z1);        return OK;
        case vr_z2:      values[(*index)++] = M(z2);        return OK;
        case vr_u1:      values[(*index)++] = M(u1);        return OK;
        case vr_u2:      values[(*index)++] = M(u2);        return OK;
        case vr_y1:      values[(*index)++] = M(y1);        return OK;
        case vr_y2:      values[(*index)++] = M(y2);        return OK;
        case vr_res1:    values[(*index)++] = M(res1);      return OK;
        case vr_res2:    values[(*index)++] = M(res2);      return OK;
        default:
            logError(comp, "Get Float64 is not allowed for value reference %u.", vr);
            return Error;
    }
}

Status setFloat64(ModelInstance* comp, ValueReference vr, const double values[], size_t nValues, size_t* index) {

    ASSERT_NVALUES(1);

    switch (vr) {
        case vr_x1: M(x1) = values[(*index)++]; return OK;
        case vr_x2: M(x2) = values[(*index)++]; return OK;
        case vr_z1: M(z1) = values[(*index)++]; return OK;
        case vr_z2: M(z2) = values[(*index)++]; return OK;
        case vr_u1: M(u1) = values[(*index)++]; return OK;
        case vr_u2: M(u2) = values[(*index)++]; return OK;

        default:
            logError(comp, "Set Float64 is not allowed for value reference %u.", vr);
            return Error;
    }
}

size_t getNumberOfContinuousStates(ModelInstance* comp) {
    UNUSED(comp);
    return 2;
}

Status getContinuousStates(ModelInstance *comp, double x[], size_t nx) {
    UNUSED(nx);
    x[0] = M(x1);
    x[1] = M(x2);
    return OK;
}

Status setContinuousStates(ModelInstance *comp, const double x[], size_t nx) {
    UNUSED(nx);
    M(x1) = x[0];
    M(x2) = x[1];
    calculateValues(comp);
    return OK;
}

Status getDerivatives(ModelInstance *comp, double dx[], size_t nx) {
    UNUSED(nx);
    calculateValues(comp);
    dx[0] = M(der_x1);
    dx[1] = M(der_x2);
    return OK;
}

Status eventUpdate(ModelInstance *comp) {

    comp->valuesOfContinuousStatesChanged   = false;
    comp->nominalsOfContinuousStatesChanged = false;
    comp->terminateSimulation               = false;
    comp->nextEventTimeDefined              = false;

    return OK;
}
