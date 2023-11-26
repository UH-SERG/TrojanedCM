static int wavpack_decode_frame(AVCodecContext *avctx,

                            void *data, int *data_size,

                            AVPacket *avpkt)

{

    WavpackContext *s = avctx->priv_data;

    const uint8_t *buf = avpkt->data;

    int buf_size = avpkt->size;

    int frame_size;

    int samplecount = 0;



    s->block = 0;

    s->samples_left = 0;

    s->ch_offset = 0;



    if(s->mkv_mode){

        s->samples = AV_RL32(buf); buf += 4;

    }

    while(buf_size > 0){

        if(!s->multichannel){

            frame_size = buf_size;

        }else{

            if(!s->mkv_mode){

                frame_size = AV_RL32(buf) - 12; buf += 4; buf_size -= 4;

            }else{

                if(buf_size < 12) //MKV files can have zero flags after last block

                    break;

                frame_size = AV_RL32(buf + 8) + 12;

            }

        }

        if(frame_size < 0 || frame_size > buf_size){

            av_log(avctx, AV_LOG_ERROR, "Block %d has invalid size (size %d vs. %d bytes left)\n",

                   s->block, frame_size, buf_size);

            return -1;

        }

        if((samplecount = wavpack_decode_block(avctx, s->block, data,

                                               data_size, buf, frame_size)) < 0)

            return -1;

        s->block++;

        buf += frame_size; buf_size -= frame_size;

    }

    *data_size = samplecount * avctx->channels;



    return s->samples_left > 0 ? 0 : avpkt->size;

}
