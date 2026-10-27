import logging

def setup_logging(level:str):
    level = level.upper()
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    logging.basicConfig( #你需要调用 logging.basicConfig，把这些参数真正喂给 Python 的日志系统
        level=level,
        format=log_format,
        handlers=[logging.StreamHandler()]
    )