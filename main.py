from urllib import request, parse
import argparse
import json

parser = argparse.ArgumentParser()
# parser.add_argument('--stb_id', type=str, required=True, help='ID of set-top box')
# parser.add_argument('--stb_mac', type=str, required=True, help='MAC address of set-top box')
# parser.add_argument('--user_id', type=str, required=True, help='User ID')
parser.add_argument('--user_token', type=str, required=True, help='user token, acquired by sniffing the traffic')
parser.add_argument('--auth_server', type=str, required=True, help='Domain of authentication server, dont forget https:// and port. e.g. https://210.13.0.147:8080')
parser.add_argument('--udpxy_base_url', type=str, required=False, default=None, help='The prefix url of udpxy. e.g. http://192.168.2.1:4022/udp/ do not forget the last slash"/". If you dont use udpxy, leave this blank.')
parser.add_argument('--output_channel_playlist_filename', type=str, required=False, default='iptv_channel.m3u', help='The output file name of m3u playlist')
args = parser.parse_args()

# REQUEST_URL_OPEN = parse.urljoin(args.auth_server, '/bj_stb/V1/STB/open')
# REQUEST_URL_AUTHENTICATOR = parse.urljoin(args.auth_server, '/bj_stb/V1/STB/userAuthenticator')
REQUEST_URL_CHANNEL_ACQUIRE = parse.urljoin(args.auth_server, '/bj_stb/V1/STB/channelAcquire')

def action_channel_acquire(user_token):
    data = json.dumps({
        'UserToken': user_token
    }).encode('utf8')
    req = request.Request(url=REQUEST_URL_CHANNEL_ACQUIRE, data=data, method='post')
    with request.urlopen(req) as res:
        return json.loads(res.read().decode('utf8'))
    pass

def process_channel_list(channel_acquire_result_json):
    def wrap(item):
        channel_url = item['channelURL'].replace('igmp://', 'rtp://') if args.udpxy_base_url is None else item['channelURL'].replace('igmp://', 'http://192.168.2.1:4022/udp/')
        return {
            'channel_id': item['channelID'],
            'user_channel_id': item['userChannelID'],
            'channel_url': channel_url,
            'channel_name': item['channelName'],
        } 
    if channel_acquire_result_json['errorMsg'] is not None:
        raise Exception('Error when acquiring channels: {e}', e=channel_acquire_result_json['errorMsg'])
    channel_list = [wrap(item) for item in channel_acquire_result_json['channleInfoStruct']]
    return channel_list

def generate_playlist_file(out_fn, channel_list, is_sorted=True):
    # _ = [print(item['channel_url']) for item in channel_list]
    if is_sorted:
        channel_list = sorted(channel_list, key=lambda item: item['user_channel_id'])
    with open(out_fn, 'w') as out_f:
        out_f.write('#EXTM3U name="bj-unicom-iptv"\n\n')
        out_f.write('\n'.join(['#EXTINF:-1,{c_name}\n{c_url}\n'.format(c_name=item['channel_name'], c_url=item['channel_url']) for item in channel_list]))

    pass

def main():
    print('Logging...')
    channel_acquire_result_json = action_channel_acquire(args.user_token)
    print('Acquiring channel list')
    channel_list = process_channel_list(channel_acquire_result_json)
    print('Writing {c} channels into file {f}'.format(c=len(channel_list), f=args.output_channel_playlist_filename))
    generate_playlist_file(args.output_channel_playlist_filename, channel_list)
    print('Done!\n\n')

if __name__ == '__main__':
    main()