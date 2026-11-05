#include "config.h"
#include "model.h"


// Resistance of the main load for the current value of the discrete variable shed
static double mainLoadResistance(ModelInstance *comp) {
    return M(shed) ? M(RShed) : M(R);
}

// Causalized form of the residual, 0 = R*i - v  =>  i = v/R
//
// The current follows from the state v and the discrete variable shed alone. It
// is only used in ODE mode and during initialization. In DAE mode the importer
// solves the residual for i, also during the event iteration.
static double causalizedCurrent(ModelInstance *comp) {
    return M(v) / mainLoadResistance(comp);
}

void setStartValues(ModelInstance *comp) {
    M(v)     = 1.0;
    M(der_v) = 0;
    M(i)     = 1.0;
    M(C)     = 1.0;
    M(R)     = 1.0;
    M(RShed) = 10.0;
    M(RAux)  = 2.0;
    M(vShed) = 0.5;
    M(iMax)  = 0.2;
    M(res1)  = 0;
    M(g1)    = 0;
    M(g2)    = 0;
    M(shed)  = false;
    M(tripped) = false;
    M(tripCondition) = false;
}

Status calculateValues(ModelInstance *comp) {

    if (comp->state == InitializationMode) {
        // The discrete variables follow the start values. pre(tripCondition) is
        // initialized with the condition, so the when-equation does not fire at
        // the initial time, and tripped keeps its start value.
        //
        // Initialization in DAE mode is not fully specified by the layered
        // standard. This FMU initializes in ODE mode, also when DAE mode is
        // enabled, and leaves a consistent value of i for the importer.
        M(shed) = M(v) < M(vShed);
        M(i) = causalizedCurrent(comp);
        M(tripCondition) = M(shed) && M(i) > M(iMax);
    }

    if (!M(ode_dae)) {
        // ODE mode: the residual is solved analytically for the main load current
        M(i) = causalizedCurrent(comp);
    }

    M(der_v) = (-M(i) - (M(tripped) ? 0.0 : M(v) / M(RAux))) / M(C);

    // residual of the main load
    M(res1) = mainLoadResistance(comp) * M(i) - M(v);

    // Event indicators. In DAE mode g2 uses the current solved by the importer, so
    // the crossing is located up to the tolerance of that solution.
    M(g1) = M(v) - M(vShed);
    M(g2) = M(i) - M(iMax);

    return OK;
}

Status getBoolean(ModelInstance* comp, ValueReference vr, bool values[], size_t nValues, size_t* index) {

    ASSERT_NVALUES(1);

    calculateValues(comp);

    switch (vr) {
        case vr_shed:    values[(*index)++] = M(shed);    return OK;
        case vr_tripped: values[(*index)++] = M(tripped); return OK;
        case vr_ode_dae: values[(*index)++] = M(ode_dae); return OK;
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
        case vr_time:  values[(*index)++] = comp->time; return OK;
        case vr_v:     values[(*index)++] = M(v);       return OK;
        case vr_der_v: values[(*index)++] = M(der_v);   return OK;
        case vr_i:     values[(*index)++] = M(i);       return OK;
        case vr_C:     values[(*index)++] = M(C);       return OK;
        case vr_R:     values[(*index)++] = M(R);       return OK;
        case vr_RShed: values[(*index)++] = M(RShed);   return OK;
        case vr_RAux:  values[(*index)++] = M(RAux);    return OK;
        case vr_vShed: values[(*index)++] = M(vShed);   return OK;
        case vr_iMax:  values[(*index)++] = M(iMax);    return OK;
        case vr_res1:  values[(*index)++] = M(res1);    return OK;
        case vr_g1:    values[(*index)++] = M(g1);      return OK;
        case vr_g2:    values[(*index)++] = M(g2);      return OK;
        default:
            logError(comp, "Get Float64 is not allowed for value reference %u.", vr);
            return Error;
    }
}

Status setFloat64(ModelInstance* comp, ValueReference vr, const double values[], size_t nValues, size_t* index) {

    ASSERT_NVALUES(1);

    switch (vr) {
        case vr_v:     M(v)     = values[(*index)++]; return OK;
        case vr_i:     M(i)     = values[(*index)++]; return OK;
        case vr_C:     M(C)     = values[(*index)++]; return OK;
        case vr_R:     M(R)     = values[(*index)++]; return OK;
        case vr_RShed: M(RShed) = values[(*index)++]; return OK;
        case vr_RAux:  M(RAux)  = values[(*index)++]; return OK;
        case vr_vShed: M(vShed) = values[(*index)++]; return OK;
        case vr_iMax:  M(iMax)  = values[(*index)++]; return OK;
        default:
            logError(comp, "Set Float64 is not allowed for value reference %u.", vr);
            return Error;
    }
}

size_t getNumberOfContinuousStates(ModelInstance* comp) {
    UNUSED(comp);
    return 1;
}

Status getContinuousStates(ModelInstance *comp, double x[], size_t nx) {
    UNUSED(nx);
    x[0] = M(v);
    return OK;
}

Status setContinuousStates(ModelInstance *comp, const double x[], size_t nx) {
    UNUSED(nx);
    M(v) = x[0];
    calculateValues(comp);
    return OK;
}

Status getDerivatives(ModelInstance *comp, double dx[], size_t nx) {
    UNUSED(nx);
    calculateValues(comp);
    dx[0] = M(der_v);
    return OK;
}

size_t getNumberOfEventIndicators(ModelInstance* comp) {
    UNUSED(comp);
    return 2;
}

Status getEventIndicators(ModelInstance *comp, double z[], size_t nz) {
    UNUSED(nz);
    calculateValues(comp);
    z[0] = M(g1);
    z[1] = M(g2);
    return OK;
}

// One pass of the event iteration. The discrete equations have to see a current
// that belongs to the new value of shed:
//
//     shed -> i -> tripCondition -> tripped
//
// ODE mode: the FMU computes i itself, so one pass evaluates the whole chain.
//
// DAE mode: the importer owns i, so the chain is split into two layers. A pass
// that changes shed stops there and requests another pass, and the importer has
// to solve the residual before it calls this function again. Evaluating the
// when-equation with the old value of i would latch tripped although the current
// may have dropped below iMax in this very event.
Status eventUpdate(ModelInstance *comp) {

    const bool preShed          = M(shed);
    const bool preTripped       = M(tripped);
    const bool preTripCondition = M(tripCondition);

    comp->valuesOfContinuousStatesChanged   = false;
    comp->nominalsOfContinuousStatesChanged = false;
    comp->terminateSimulation               = false;
    comp->nextEventTimeDefined              = false;

    comp->isDirtyValues = true;

    // layer 1
    M(shed) = M(v) < M(vShed);

    if (M(ode_dae) && M(shed) != preShed) {
        comp->newDiscreteStatesNeeded = true;
        return OK;
    }

    if (!M(ode_dae)) {
        M(i) = causalizedCurrent(comp);
    }

    // layer 2
    M(tripCondition) = M(shed) && M(i) > M(iMax);

    if (M(tripCondition) && !preTripCondition) {
        M(tripped) = true;
    }

    // Run one more pass after any change, until the discrete variables are stable
    comp->newDiscreteStatesNeeded = M(shed) != preShed
                                 || M(tripped) != preTripped
                                 || M(tripCondition) != preTripCondition;

    return OK;
}
