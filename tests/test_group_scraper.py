import pytest
import responses
from src.facebook_group_scraper import GroupScraper

reply_url = [
    (
        1,
        "https://m.facebook.com/comment/replies/?ctoken=6672174939467489_6679570298727953&count=1&curr&pc=1&isinline&initcomp&ft_ent_identifier=6672174939467489&eav=Afb48ex-pC6nF3g44xwdFz64eqy7gjHgkqk-3o4nnSoypdG_h5b89Ct2T3xKDkrdgEw&av=0&gfid=AQCL5swFIQYluOWutYg&refid=18&__tn__=R-R",
    ),
    (
        2,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6681512655200384&count=9&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=Afb_6FM7CKF_fX9vSNVTtxbtanAtYH0RHQMwBNDs8DLRjJMtwBlrOGhkhVoRFRVzz0A&av=0&gfid=AQBn59Bt5wO7f_l8Vhw&refid=18&__tn__=R-R",
    ),
    (
        3,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6681539348531048&count=3&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=AfZeGaBnJXxRig0L5DdnxojISQic-p6O8VyZMFnySmH9jz-zr2bTlLD_DBTd6sIfnL8&av=0&gfid=AQDNoyHSONS9F07WtwA&refid=18&__tn__=R-R",
    ),
    (
        4,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6681656065186043&count=2&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=Afa66gw7OXTeB0yWQkqwpKJx2G5FgZiPBf3BWZ-psLWUJxDKBAKfwe8bMDtLOT1EKu4&av=0&gfid=AQC3c7tgbRkWBgoGfl0&refid=18&__tn__=R-R",
    ),
    (
        5,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6681661045185545&count=7&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=AfbvDNH5r7neaHY17uCYo2d3olIfZOXdEV8h2kqFBqHd0-59GRfMhqC5rVNwO8sJI7c&av=0&gfid=AQB7NtSgS_mkbSEXmq4&refid=18&__tn__=R-R",
    ),
    (
        6,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6681759075175742&count=1&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=AfZwdtXn6l5bNgNPWfMsESV1fn5uXwxEdTfaYGOSUv1Rjmg6p9C2GdTI03ewIAVYrVI&av=0&gfid=AQCh6hRcQ3mbtJQL_1w&refid=18&__tn__=R-R",
    ),
    (
        7,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6681893828495600&count=1&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=AfZnF-gfH9KE2Bxz3SrdRbglRUWiCuYhsrpJ0Z5sktoNyCxc2eSknNarXqNFE4krp04&av=0&gfid=AQD-VGKUpdb2srv6604&refid=18&__tn__=R-R",
    ),
    (
        8,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6681983561819960&count=1&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=AfbcvXNJkP99Rc44sY4g5oXqgErTac6HVSyiYXOqFn9-uCuiQYuVfZrAofmzYgb2HIM&av=0&gfid=AQAjpZCpY1TcclKUErE&refid=18&__tn__=R-R",
    ),
    (
        9,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6681983561819960&count=1&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=AfbcvXNJkP99Rc44sY4g5oXqgErTac6HVSyiYXOqFn9-uCuiQYuVfZrAofmzYgb2HIM&av=0&gfid=AQAjpZCpY1TcclKUErE&refid=18&__tn__=R-R",
    ),
    (
        10,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6682948931723423&count=5&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=AfZTxuMXZv4DTrHcV72PSwKHL779QafWvWI2wjF9f2K_opxonoZIDQDHlFzGkwvDXu0&av=0&gfid=AQB4AwFYzJe9QcjBiEg&refid=18&__tn__=R-R",
    ),
    (
        11,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6683780204973629&count=1&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=Afae90lX2s0sjJfkfMZ-zKG3kIYHHWc5g2afg8SxdwtnIL7jnOsRVgqhoD1G_bFu2Ok&av=0&gfid=AQCbE98dpCwicZ32cXA&refid=18&__tn__=R-R",
    ),
    (
        12,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6683847561633560&count=1&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=AfY2ioGiLewSGFLVlGh9FK2CG5k0gS9NVvvSaAYvQtXXQd1wSTR8fGPM1fCvYhepijY&av=0&gfid=AQC7YmWunvFgO-MQDVo&refid=18&__tn__=R-R",
    ),
    (
        13,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6684360771582239&count=1&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=AfagCbDOgj__W8LLxYCm85FB2x89Wx9t_esxXOCGo03e2wORO-4YlLHvbjDPKy8oBxs&av=0&gfid=AQATaQiVk3u2rJXE8s8&refid=18&__tn__=R-R",
    ),
    (
        14,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6681287158556267&count=4&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=Afb8hIVxMjWDp6hWg5vhlgmwGYv-2l8f0xm7kHEXUDA1Y6Tek0eJzD80m3TvE_xKrEg&av=0&gfid=AQD-zqVinvlZtGfkOlA&refid=18&__tn__=R-R",
    ),
    (
        15,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6681307291887587&count=6&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=AfaDUMJWoobqJlYK_zvAhyrdqjntSwr2FAxcpG9udCJpZcBXuN9U1m8EtWZ1ZwuN0g0&av=0&gfid=AQBAXE_40gtEhcQsnvs&refid=18&__tn__=R-R",
    ),
    (
        16,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6681362555215394&count=3&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=AfYq86ujmHvpvxvb8hRLxQy4Y4W2Oss9dyyB9h0RrUAjqKv-gz0A4Wmrz2szgEBmLCk&av=0&gfid=AQB-OI3WZELujo5mAm8&refid=18&__tn__=R-R",
    ),
    (
        17,
        "https://m.facebook.com/comment/replies/?ctoken=6681059068579076_6681390341879282&count=5&curr&pc=1&isinline&initcomp&ft_ent_identifier=6681059068579076&eav=AfZpWF2KIxTiwzVwHMh_JuYabttaxNzQmo4xRC0PVyO2Q9jJ2VTWP4cMe-QNQuVZZiA&av=0&gfid=AQDbd66zLc8VrRcrdB0&refid=18&__tn__=R-R",
    ),
]


@responses.activate
def test_group_scraper():
    responses.add(
        responses.GET,
        "https://m.facebook.com/groups/1260448967306807",
        status=200,
        body=open("tests/data/group.html").read(),
    )

    responses.add(
        responses.GET,
        "https://m.facebook.com/6681059068579076",
        status=200,
        body=open("tests/data/post.html").read(),
    )

    responses.add(
        responses.GET,
        "https://m.facebook.com/groups/1260448967306807/permalink/6681059068579076/?p=30&refid=18&__tn__=-R",
        status=200,
        body=open("tests/data/comments_next_page.html").read(),
    )

    for i, url in reply_url:
        responses.add(
            responses.GET,
            url,
            status=200,
            body=open(f"tests/data/replies_{i}.html").read(),
        )

    scraper = GroupScraper(
        group_url="1260448967306807",
        page_cursor=None,
        fetch_comment=True,
        fetch_reply=True,
        page_sleep_secs=0,
        comment_sleep_secs=0,
        reply_sleep_secs=0,
    )
    for post in scraper.start():
        assert post["post_id"] == "6681059068579076"
        assert post["group_id"] == "1260448967306807"
        assert post["publish_time"] == 1681521458
        assert post["author_id"] == "100033148069290"
        assert post["author_name"] == "Wen Wen"
        assert post["post_list"] is None
        assert post["content"] == [
            "房子太小之選擇咖啡機",
            " 買了五年的半自動咖啡機，",
            " 出現漏水已經ㄧ陣子了，",
            " 某天忽然完全不能出水，",
            " 我拿去好市多送修回報說沒零件不維修了，",
            " 我便再線上買了這一台，",
            " 雖然也小小台，但剛好放進我的小空間，",
            " 很有質感、咖啡超好喝，",
            " 因爲廠商訴求說裡面有支濾心會處理水質，",
            " 好喝到我晚上都還想泡一杯來喝，",
            "… ",
            "更多",
            " 雖然水箱不大又在後面，",
            " 但濃縮咖啡每次用水量很少，不用常加水。",
            " 對我來說，非常滿意半自動咖啡機，",
            " 有空可以打奶泡",
            " 趕上班直接加冰牛奶帶著走，",
            " 好喝又方便。",
        ]
        assert post["likes"] == 1698
        assert post["comments"] == 37
        assert post["comments_full"][0]["comment_id"] == "6681512655200384"

        break
