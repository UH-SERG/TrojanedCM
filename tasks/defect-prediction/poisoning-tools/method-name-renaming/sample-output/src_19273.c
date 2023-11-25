static int flv_data_packet(AVFormatContext *s, AVPacket *pkt,

                           int64_t dts, int64_t next)

{

    AVIOContext *pb = s->pb;

    AVStream *st    = NULL;

    char buf[20];

    int ret = AVERROR_INVALIDDATA;

    int i, length = -1;



    switch (avio_r8(pb)) {

    case AMF_DATA_TYPE_MIXEDARRAY:

        avio_seek(pb, 4, SEEK_CUR);

    case AMF_DATA_TYPE_OBJECT:

        break;

    default:

        goto skip;

    }



    while ((ret = amf_get_string(pb, buf, sizeof(buf))) > 0) {

        AMFDataType type = avio_r8(pb);

        if (type == AMF_DATA_TYPE_STRING && !strcmp(buf, "text")) {

            length = avio_rb16(pb);

            ret    = av_get_packet(pb, pkt, length);

            if (ret < 0)

                goto skip;

            else

                break;

        } else {

            if ((ret = amf_skip_tag(pb, type)) < 0)

                goto skip;

        }

    }



    if (length < 0) {

        ret = AVERROR_INVALIDDATA;

        goto skip;

    }



    for (i = 0; i < s->nb_streams; i++) {

        st = s->streams[i];

        if (st->codec->codec_type == AVMEDIA_TYPE_DATA)

            break;

    }



    if (i == s->nb_streams) {

        st = create_stream(s, AVMEDIA_TYPE_DATA);

        if (!st)

            return AVERROR_INVALIDDATA;

        st->codec->codec_id = AV_CODEC_ID_TEXT;

    }



    pkt->dts  = dts;

    pkt->pts  = dts;

    pkt->size = ret;



    pkt->stream_index = st->index;

    pkt->flags       |= AV_PKT_FLAG_KEY;



skip:

    avio_seek(s->pb, next + 4, SEEK_SET);



    return ret;

}
