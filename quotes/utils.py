import hashlib
import hmac
from math import sqrt

from django.conf import settings


def get_client_ip(request) -> str:
    """IP клиента: из заголовка доверенного прокси, если он настроен, иначе REMOTE_ADDR."""
    header = getattr(settings, 'CLIENT_IP_HEADER', '')
    if header and request.META.get(header):
        return request.META[header].split(',')[-1].strip()[:45]
    return (request.META.get('REMOTE_ADDR') or '')[:45]


def make_fingerprint(request) -> str:
    """Отпечаток для антидублей голосов: один голос за цитату с одного IP.
    Cookie и User-Agent не учитываются, потому что клиент может менять их при каждом запросе.
    Приватности ради IP хранится только в виде HMAC.
    """
    ip = get_client_ip(request).encode('utf-8', 'ignore')
    return hmac.new(settings.SECRET_KEY.encode('utf-8'), ip, hashlib.sha256).hexdigest()


def wilson_lower_bound(up: int, down: int, confidence: float = 0.95) -> float:
    n = up + down
    if n == 0:
        return 0.0
    from math import erf, sqrt

    z = 1.959963984540054  
    phat = up / n
    denom = 1 + z*z/n
    num = phat + z*z/(2*n) - z*sqrt((phat*(1-phat) + z*z/(4*n))/n)
    return num / denom
