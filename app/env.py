import logging
logger = logging.getLogger(__name__)


class UnsupportedMode(Exception):
    """Raised when the user requests a rendering mode not supported by the
    environment.
    """
    pass


class Env:
    def __new__(cls, *args, **kwargs):
        # We use __new__ since we want the env author to be able to
        # override __init__ without remembering to call super.
        env = super(Env, cls).__new__(cls)
        env._env_closer_id = env_closer.register(env)
        env._closed = False

        # Will be automatically set when creating an environment via 'make'
        return env

    # Set this in SOME subclasses
    metadata = {'render.modes': []}
    reward_range = (-np.inf, np.inf)
    
    # Set these in ALL subclasses
    action_space = None
    observation_space = None

    # Override in ALL subclasses
    def _step(self, action): raise NotImplementedError
    def _reset(self): raise NotImplementedError
    def _render(self, mode='human', close=False): return

    def step(self, action):
        return self._step(action)

    def reset(self):
        return self._reset()

    def render(self, mode='human', close=False):
        if not close: # then we have to check rendering mode
            modes = self.metadata.get('render.modes', [])
            if len(modes) == 0:
                raise error.UnsupportedMode('{} does not support rendering (requested mode: {})'.format(self, mode))
            elif mode not in modes:
                raise error.UnsupportedMode('Unsupported rendering mode: {}. (Supported modes for {}: {})'.format(mode, self, modes))
        return self._render(mode=mode, close=close)


class SamurAI(Env):
    def __init__(self):
        self.viewer = None

    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        if self.viewer is None:
            screen_width = 800
            screen_height = 600
            self.viewer = renderer.Viewer((screen_width, screen_height))
            
