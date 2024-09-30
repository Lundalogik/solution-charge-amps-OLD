import logging

logger = logging.getLogger(__name__)


def default_config():
    """Returns the default values for configuration parameters for this package

    The resulting configuration will be available under
    `lime_config.config['plugins']['solution_charge_amps']`

    The values here can be overridden in the service's config file.
    """

    return {}


try:
    from .endpoints import register_blueprint  # noqa
except ImportError:
    logger.info('solution_charge_amps doesn\'t implement any custom '
                'endpoints')

try:
    from .event_handlers import register_event_handlers  # noqa
except ImportError:
    logger.info('solution_charge_amps doesn\'t implement any event '
                'handlers')

try:
    from .limeobject_classes import register_limeobject_classes  # noqa
except ImportError:
    logger.info('solution_charge_amps doesn\'t implement any '
                'limeobject classes')

try:
    from .web_components import register_web_components  # noqa
except ImportError:
    logger.info('solution_charge_amps doesn\'t implement any '
                'web-components')

try:
    from .translations import register_translations  # noqa
except ImportError:
    logger.info('solution_charge_amps doesn\'t contain any '
                'translations')

try:
    from .config import register_config  # noqa
except ImportError:
    logger.info('solution_charge_amps doesn\'t contain any config')

try:
    from .tasks import get_task_modules  # noqa
except ImportError:
    logger.info('solution_charge_amps doesn\'t implement any '
                'async tasks')

try:
    from .tasks import register_scheduled_tasks  # noqa
except ImportError:
    logger.info('solution_charge_amps doesn\'t contain any '
                'scheduled tasks')


def register_static_content():
    '''
    Returns a list with tuples:
        (route, path_to_static_content).

    This function is called from lime-webserver to find out where the proxy
    should create symlinks for the static content for this package.

    The static content in the `path_to_static_content` will be
    available through the webserver at
    `/<rooturl-to-app>/static/<package-name>/<route>`.

    If you want to serve static content from a module in this package,
    add the function `register_static_content` to the module. The function
    takes no arguments and shall return a list with tuples in the same form as
    this function.
    '''
    static_filepaths = []
    try:
        from .web_components import register_static_content as wc_reg_static
        static_filepaths += wc_reg_static()
    except ImportError:
        logger.info('solution_charge_amps doesn\'t contain any'
                    'static content')
    return static_filepaths
