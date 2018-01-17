from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException


def sendsms(username, apikey, to, message):
    gateway = AfricasTalkingGateway(username, apikey)
    try:
        gateway.sendMessage(to, message)

    except AfricasTalkingGatewayException as e:
        return 'Encountered an error while sending: %s' % str(e)