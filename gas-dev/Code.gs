const CHANNEL_ACCESS_TOKEN = '';

/* * 1. 网页入口函数
 * 当用户访问这个 Web App 的 URL 时，显示 index.html
 */
function doGet(e) {
  // 创建 HTML 模板
  let template = HtmlService.createTemplateFromFile('index');
  
  // 允许 HTML 页面能够在移动端自适应显示
  return template.evaluate()
      .addMetaTag('viewport', 'width=device-width, initial-scale=1')
      .setTitle('貸出確認');
}

/* * 2. 借出处理函数 (被前端 HTML 调用)
 * 接收 userId 和 containerId，写入表格并发送通知
 */
function processBorrow(userId, containerId) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('Log');
  
  // 1. 写入数据库 (Google Sheet)
  const timestamp = new Date();
  sheet.appendRow([timestamp, userId, containerId, 'BORROWED']);
  
  // 2. 调用 LINE API 发送推送消息
  pushMessageToUser(userId, containerId);
  
  return "SUCCESS"; // 告诉前端搞定了
}

/*
 * 3. 辅助函数：发送 LINE 推送消息
 */
function pushMessageToUser(userId, containerId) {
  const url = 'https://api.line.me/v2/bot/message/push';
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + CHANNEL_ACCESS_TOKEN
  };
  
  const postData = {
    'to': userId,
    'messages': [
      {
        'type': 'text',
        'text': '貸出完了しました！\n容器番号: ' + containerId + '\n美味しく食べてください！🍱'
      }
    ]
  };
  
  const options = {
    'method': 'post',
    'headers': headers,
    'payload': JSON.stringify(postData)
  };
  
  try {
    UrlFetchApp.fetch(url, options);
  } catch (e) {
    Logger.log('Failed to send the massage: ' + e.toString());
  }
}