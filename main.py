import logging
import pulsectl
from bluetooth import BTDevice
from cider import CiderAPI
import time

from wakepy import keep

BT_MAC_ADDRESS = '28:C3:BC:B4:48:75'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

cider = CiderAPI('xmgfmusy6iidedoo3gjk6le1')
speaker = BTDevice(BT_MAC_ADDRESS)

def select_sink_for_device(mac_address):
    with pulsectl.Pulse('sleep_well') as pulse:
        for sink in pulse.sink_list():
            if sink.proplist.get('device.name') == 'bluez_card.' + mac_address.replace(':', '_'):
                logger.info(f'Changing sink to {sink.name}')
                pulse.default_set(sink)
                
                # also change the volume
                logging.info('Setting volume to 150%')
                pulse.volume_set_all_chans(sink, 1.5)
                break
            

def sleep_well():
    if cider.is_active():
        logger.info('Cider is active')
        
        # disable autoplay
        if cider.get_autoplay_state():
            logger.info('Disabling autoplay')
            cider.toggle_autoplay()
            
        cider.set_volume(100) # returns 404 but whatever
        
        # select the sink for the device
        select_sink_for_device(BT_MAC_ADDRESS)
        
        cider.play_url('https://music.apple.com/br/playlist/chuva-infinita/pl.c724b210445541e7a306561d89761ca2')
        
        with keep.running():
            logger.info('Sleeping for 1 hour')
            time.sleep(3600)
        
            logger.info('Pausing playback')
            cider.pause()
        
            logger.info('Disconnecting speaker')
            speaker.disconnect_device()
    else:
        logger.info('Cider is not active')
    

def main():
    if not speaker.is_connected():
        logger.info('Connecting to speaker')
        try:
            speaker.connect_device()
            sleep_well()
        except Exception as e:
            logger.info('Failed to connect to speaker')
            logger.exception(e)
    else:
        logger.info('Speaker is already connected')
        sleep_well()
            
if __name__ == '__main__':
    main()