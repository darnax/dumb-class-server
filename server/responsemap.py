
ResponseMap = {}

# 1xx
ResponseMap[100] = 'Continue'
ResponseMap[101] = 'Switching Protocols'
ResponseMap[102] = 'Processing'

# 2xx
ResponseMap[200] = 'OK'
ResponseMap[201] = 'Created'
ResponseMap[202] = 'Accepted'
ResponseMap[203] = 'Non-Authoritative Information'
ResponseMap[204] = 'No Content'
ResponseMap[205] = 'Reset Content'
ResponseMap[206] = 'Partial Content'
ResponseMap[207] = 'Multi-Status'
ResponseMap[208] = 'Already Reported'
ResponseMap[226] = 'IM Used'

# 3xx
ResponseMap[300] = 'Multiple Choices'
ResponseMap[301] = 'Moved Permanently'
ResponseMap[302] = 'Found'
ResponseMap[303] = 'See Other'
ResponseMap[304] = 'Not Modified'
ResponseMap[305] = 'Use Proxy'
ResponseMap[306] = 'Switch Proxy'
ResponseMap[307] = 'Temporary Redirect'
ResponseMap[308] = 'Permanent Redirect'

# 4xx
ResponseMap[400] = 'Bad Request'
ResponseMap[401] = 'Unauthorized'
ResponseMap[402] = 'Payment Required'
ResponseMap[403] = 'Forbidden'
ResponseMap[404] = 'Not Found'
ResponseMap[405] = 'Method Not Allowed'
ResponseMap[406] = 'Not Acceptable'
ResponseMap[407] = 'Proxy Authentication Required'
ResponseMap[408] = 'Request Timeout'
ResponseMap[409] = 'Conflict'
ResponseMap[410] = 'Gone'
ResponseMap[411] = 'Length Required'
ResponseMap[412] = 'Precondition Failed'
ResponseMap[413] = 'Request Entity Too Large'
ResponseMap[414] = 'Request-URI Too Long'
ResponseMap[415] = 'Unsupported Media Type'
ResponseMap[416] = 'Requested Range Not Satisfiable'
ResponseMap[417] = 'Expectation Falied'
ResponseMap[418] = 'I\'m a teapot'
ResponseMap[422] = 'Unprocessable Entity'
ResponseMap[423] = 'Locked'
ResponseMap[424] = 'Failed Dependency'
ResponseMap[426] = 'Upgrade Required'
ResponseMap[428] = 'Precondition Required'
ResponseMap[429] = 'Too Many Requests'
ResponseMap[431] = 'Request Header Fields Too Large'
ResponseMap[451] = 'Unavailable For Legal Reasons'

# 5xx
ResponseMap[500] = 'Internal Server Error'
ResponseMap[501] = 'Not Implemented'
ResponseMap[502] = 'Bad Gateway'
ResponseMap[503] = 'Service Unavailable'
ResponseMap[504] = 'Gateway Timeout'
ResponseMap[505] = 'HTTP Version Not Supported'
ResponseMap[506] = 'Variant Also Negotiates'
ResponseMap[507] = 'Insufficient Shorage'
ResponseMap[508] = 'Loop Detected'
ResponseMap[509] = 'Bandwidth Limit Exceeded'
ResponseMap[510] = 'Not Extended'
ResponseMap[511] = 'Network Authentication Required'
