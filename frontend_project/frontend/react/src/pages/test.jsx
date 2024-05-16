import React, { useState } from 'react';

function TestApp() {
  // 配列を useState で管理
  const [items, setItems] = useState(["リンゴ", "バナナ", "オレンジ"]);

  // アイテムを削除する関数
  const removeItem = index => {
    // filter を使って index に一致しないアイテムだけを新たな配列として設定
    setItems(items.filter((item, i) => i !== index));
    console.log(items.index);
    console.log(items);
  };

  return (
    <div>
      <h1>果物リスト</h1>
      <ul>
        {items.map((item, index) => (
          <li key={index}>
            {item}
            <button onClick={() => removeItem(index)}>削除</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TestApp;
