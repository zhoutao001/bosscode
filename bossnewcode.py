# 导入自动化模块
from DrissionPage import ChromiumPage
import csv
import json
# 创建文件
f = open('data3.csv', mode='w', encoding='utf-8', newline='')
# 字典写入 f创建文件对象，fieldnames字段名
csv_writer = csv.DictWriter(f, fieldnames=[
    '职位',
    '公司',
    '规模',
    '薪资',
    '城市',
    '区域',
    '经验',
    '学历',
    '领域',
    '技能',
    '福利',
])
# 写入表头
csv_writer.writeheader()
# 打开浏览器
driver = ChromiumPage()
# 监听数据包
driver.listen.start('wapi/zpgeek/search/joblist.json')
# 访问网站
driver.get('https://www.zhipin.com/web/geek/job?query=%E6%95%B0%E5%AD%97%E8%89%BA%E6%9C%AF&city=100010000')
# 循环采集
for page in range(10):
    # 把网页下滑到最下面
    driver.scroll.to_bottom()
    # 等待数据包加载
    resp = driver.listen.wait()
    # 获取数据包响应内容
    json_data = resp.response.body
    # 把招聘信息对应的jobList列表提取出来
    jobList = json_data['zpData']['jobList']
    for job in jobList:
        dit = {
            '职位': job['jobName'],
            '公司': job['brandName'],
            '规模': job['brandScaleName'],
            '薪资': job['salaryDesc'],
            '城市': job['cityName'],
            '区域': job['areaDistrict'],
            '经验': job['jobExperience'],
            '学历': job['jobDegree'],
            '领域': job['brandIndustry'],
            '技能': ','.join(job['skills']),
            '福利': ','.join(job['welfareList'])
        }
        # 写入数据
        csv_writer.writerow(dit)
        print(dit)
    # 点击下一页
    driver.ele('css:.ui-icon-arrow-right').click()
