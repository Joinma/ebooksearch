DROP TABLE IF EXISTS `ishare`;
CREATE TABLE IF NOT EXISTS `ishare`(
  `url_obj_id` VARCHAR(100) NOT NULL UNIQUE COMMENT 'md5加密后的url',
  `title` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '标题',
  `upload_people` VARCHAR(255) DEFAULT '' COMMENT '上传者',
  `score` INT(3) NOT NULL DEFAULT 0 COMMENT '评分',
  `load_num` INT(10) NOT NULL DEFAULT 0 COMMENT '下载次数',
  `read_num` INT(10) DEFAULT 0 COMMENT '查看人数',
  `comment_num` INT(10) DEFAULT 0 COMMENT '评论数',
  `collect_num` INT(10) DEFAULT 0 COMMENT '收藏数',
  `upload_time` BIGINT NOT NULL DEFAULT 0 COMMENT '上传时间',
  `crawl_time` BIGINT NOT NULL DEFAULT 0 COMMENT '爬取时间',
  `url` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '资料链接',
  `source_website` VARCHAR(255) DEFAULT '' COMMENT '来源网站',
  `type` INT(2) NOT NULL DEFAULT 0 COMMENT '文件类型，0 pdf 1 epub 2 mobi 3 doc 4 txt',
  `size` DECIMAL(5, 2) NOT NULL DEFAULT 0.00 COMMENT '文件大小',


  PRIMARY KEY (`url_obj_id`)
)ENGINE = InnoDB CHARACTER SET = utf8 COMMENT '新浪爱问分享资料'
