1. サブスクリプションの確認

 az account show


出力結果の id が、サブスクリプションID
 ---
 {
   "environmentName": "AzureCloud",
   "id": "00000000-0000-0000-0000-000000000000",
   "isDefault": true,
   "name": "Microsoft Azure XXX プラン",
   "state": "Enabled",
   "tenantId": "00000000-0000-0000-0000-000000000000",
   "user": {
     "name": "yournanme@example.com",
     "type": "user"
   }
 }
 ---


2. env の編集

env ファイルのSUBS に自分のサブスクリプションID、RNAME に利用するリソースグループ名を記載

3. 環境変数の設定

  . ./env
  echo $SUBS
  echo $RNAME

サブスクリプションIDとリソースグループ名が正しく設定されていることを確認。

4. デプロイスクリプトの実行

 ./deploy.sh -i $SUBS -g $RNAME -n $DNAME -l $LOC
 ＜中略＞
 Template has been successfully deployed
