# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os, json
from flask import Flask, request, abort, render_template
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)
import db.funddb as funddb

# set token or get from environments
def gettoken():
    data = json.load(open('config/default.json', 'r'))
    return data['wx']['token']

TOKEN = os.getenv('WECHAT_TOKEN', gettoken())
AES_KEY = os.getenv('WECHAT_AES_KEY', '')
APPID = os.getenv('WECHAT_APPID', '')

app = Flask(__name__)


@app.route('/')
def index():
    host = request.url_root
    return render_template('index.html', host=host)

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    print(signature)
    print(timestamp)
    print(nonce)
    #encrypt_type = request.args.get('encrypt_type', 'raw')
    #msg_signature = request.args.get('msg_signature', '')
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == 'GET':
        echo_str = request.args.get('echostr', '')
        return echo_str

    # POST request
    msg = parse_message(request.data)
    if msg.type == 'text':
        if msg.content == 'jj':
            chose_fund = funddb.get_chosen_fund()
            reply = create_reply(chose_fund, msg)
        else:
            reply = create_reply(msg.content, msg)        
    else:
        reply = create_reply('Sorry, can not handle this for now', msg)
    return reply.render()


if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=True)
