from restful import response_object as res

STATUS_CODES = {
    res.ResponseSuccess.SUCCESS: 200,
    res.ResponseFailure.PARAMETERS_ERROR: 400,
    res.ResponseFailure.UNAUTHORIZED: 401,
    res.ResponseFailure.FORBIDDEN: 403,
    res.ResponseFailure.RESOURCE_ERROR: 404,
    res.ResponseFailure.UNPROCESSABLE_ENTITY: 422,
    res.ResponseFailure.SYSTEM_ERROR: 500,
}
