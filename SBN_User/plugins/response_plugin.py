from rest_framework import status
from rest_framework.response import Response

successful_dict = {
    200: status.HTTP_200_OK,
    201: status.HTTP_201_CREATED,
    202: status.HTTP_202_ACCEPTED,
    203: status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
    204: status.HTTP_204_NO_CONTENT,
    205: status.HTTP_205_RESET_CONTENT,
    206: status.HTTP_206_PARTIAL_CONTENT,
    207: status.HTTP_207_MULTI_STATUS,
    208: status.HTTP_208_ALREADY_REPORTED,
    226: status.HTTP_226_IM_USED
}

error_dict = {
    400: status.HTTP_400_BAD_REQUEST,
    401: status.HTTP_401_UNAUTHORIZED,
    402: status.HTTP_402_PAYMENT_REQUIRED,
    403: status.HTTP_403_FORBIDDEN,
    404: status.HTTP_404_NOT_FOUND,
    405: status.HTTP_405_METHOD_NOT_ALLOWED,
    406: status.HTTP_406_NOT_ACCEPTABLE,
    407: status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED,
    408: status.HTTP_408_REQUEST_TIMEOUT,
    409: status.HTTP_409_CONFLICT,
    410: status.HTTP_410_GONE,
    411: status.HTTP_411_LENGTH_REQUIRED,
    412: status.HTTP_412_PRECONDITION_FAILED,
    413: status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    414: status.HTTP_414_REQUEST_URI_TOO_LONG,
    415: status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    416: status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
    417: status.HTTP_417_EXPECTATION_FAILED,
    422: status.HTTP_422_UNPROCESSABLE_ENTITY,
    423: status.HTTP_423_LOCKED,
    424: status.HTTP_424_FAILED_DEPENDENCY,
    426: status.HTTP_426_UPGRADE_REQUIRED,
    428: status.HTTP_428_PRECONDITION_REQUIRED,
    429: status.HTTP_429_TOO_MANY_REQUESTS,
    431: status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
    451: status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
}

server_error_dict = {
    500: status.HTTP_500_INTERNAL_SERVER_ERROR,
    501: status.HTTP_501_NOT_IMPLEMENTED,
    502: status.HTTP_502_BAD_GATEWAY,
    503: status.HTTP_503_SERVICE_UNAVAILABLE,
    504: status.HTTP_504_GATEWAY_TIMEOUT,
    505: status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
    506: status.HTTP_506_VARIANT_ALSO_NEGOTIATES,
    507: status.HTTP_507_INSUFFICIENT_STORAGE,
    508: status.HTTP_508_LOOP_DETECTED,
    509: status.HTTP_509_BANDWIDTH_LIMIT_EXCEEDED,
    510: status.HTTP_510_NOT_EXTENDED,
    511: status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
}

message_dict = {
    200: "Passed successfully!",
    201: "created successfully!",
    202: "accepted successfully!",
    203: "None authoritative information!",
    204: "No content!",
    205: "Reset content!",
    206: "Partial content!",
    207: "Multi status!",
    208: "Already!",
    226: "Im used!",
}

server_error_mess_dict = {
    500: "Internal server error!",
    501: "Not implemented!",
    502: "Bad gateway!",
    503: "Service unavailable!",
    504: "Gateway timeout!",
    505: "Http version not supported!",
    506: "Variant also negotiated!",
    507: "Insufficient storage!",
    508: "Loop detected!",
    509: "Bandwith limit exceeded!",
    510: "Not extended!",
    511: "Network authentication required!",
}


def handle_err(error):
    if "UNIQUE" in error:
        return "Username or email has already existed in the database!"
    elif "Could not verify token signature." in error:
        return "Could not verify token signature!"
    else:
        print(error)
        return error

def handle_mes(status_code, dicts):
    if (status_code in successful_dict):
        if str(type(dicts)) == "<class 'dict'>":
            return Response(data=dicts, status=successful_dict[status_code])
        elif str(type(dicts)) == "<class 'rest_framework.utils.serializer_helpers.ReturnList'>":
            return Response(data=dicts, status=successful_dict[status_code])
        else:
            mess = '{} {}'.format(dicts, message_dict[status_code])
            return Response({"message": mess}, status=successful_dict[status_code])

    if status_code in error_dict:
        if str(type(dicts)) == "<class 'dict'>":
            return Response(data=dicts, status=error_dict[status_code])
        else:
            return Response({"error": handle_err(str(dicts))}, status=error_dict[status_code])
    if status_code in server_error_dict:
        return Response({"message": server_error_mess_dict[status_code]}, status=server_error_dict[status_code])


def handcraft_res(status_code, *args):
    return handle_mes(
        status_code,
        args[0] if args else ""
    )
