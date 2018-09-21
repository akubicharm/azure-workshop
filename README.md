# Azureワークショップの資料
Azureサービスを利用したワークショップの資料です。
配布資料はasciidocで記載しているので、ブラウザでそのまま参照するとパラメータが展開されません。実際にワークショップで利用する場合には、asciidoctorでパラメータを反映したPDFを作成して参照してください。

## 配布資料の作成方法
asciidoctor を利用してパラメータも反映した形式でPDF化することができます。
Docker版のasciidoctor を利用してPDF化する方法は次の通りです。

1. Docker コンテナの実行
asciidock形式のファイルが保存してあるディレクトリを指定して、asciidoctorのコンテナを実行します

```
docker run -it -v [ASCIIDOC の保存してあるディレクトリ]:/documents/ asciidoctor/docker-asciidoctor
```

2. `.adoc` ファイルのPDF化
```
asciidoctor-pdf deploy-aks.adoc
```

3. コンテナからExit
`exit` コマンドを実行して、コンテナからExitします。


## ワークショップコンテンツ

### IoT テクニカルワークショップ
IoT HubとTime Series Insights, Stream Analytics, PowerBIとの連携とAzure IoT Edgeのデプロイ

[./pdf/iot-technical-workshop.pdf](./pdf/iot-technical-workshop.pdf)
