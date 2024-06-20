from evennia import DefaultChannel
from evennia.utils import logger

class ChannelLogger(DefaultChannel):
    """
    A channel that logs all messages sent to it.
    """

    def at_post_msg(self, message, **kwargs):
        # Call the parent class's at_post_msg method
        super().at_post_msg(message, **kwargs)
        
        # Log the message
        logger.log_file(message, self.get_log_filename())

    def get_log_filename(self):
        # Return a filename to log messages to
        return f"channel_{self.key.lower()}.log"

    def msg(self, message, senders=None, bypass_mute=False, **kwargs):
        # Call the parent class's msg method
        super().msg(message, senders=senders, bypass_mute=bypass_mute, **kwargs)
        
        # Log the message
        self.at_post_msg(message, **kwargs)

from evennia import create_channel

# Create a new channel
channel = create_channel("mychannel", typeclass=ChannelLogger)

# Send a message to the channel
channel.msg("Hello, world!")
                  