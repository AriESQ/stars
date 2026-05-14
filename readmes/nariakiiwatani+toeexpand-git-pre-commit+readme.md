# toeexpand-githook

git hooksのpre-commitタイミングで、stagingにあるtoeとtoxについて[toeexpand](https://docs.derivative.ca/Toeexpand)を実行し、その出力を追加でコミットします。

# How to use

`scripts`フォルダにある`pre-commit.[platform]`をあなたの`.git/hooks/`フォルダにコピーし、`pre-commit`にリネームしてください。  
環境によっては実行権限を与える必要があるかもしれません。(`chmod +x .git/hooks/pre-commit`など)

# Then what?

toeexpandで吐かれるファイル群は`ascii readable files`なので、つまりTouchDesignerのファイルの更新内容がgitで差分として読めるようになります。  
[toecollapse](https://docs.derivative.ca/Toecollapse)を使うと`.toe`や`.tox`を復元できるようなので、差分の内容次第では目でマージができるようになるかもしれません。（未検証）  
複数人でTouchDesignerのプロジェクトをやるときに、とりあえず導入しておくともしもの時に「入れててよかった」的なものくらいにはになってくれるかもしれません。

`toeexpand`を使わず、もうすこしhuman-readableな出力にしたものも作っています。  
-> [VersioningTouchDesignerNetwork](https://github.com/nariakiiwatani/VersioningTouchDesignerNetwork)  
こちらには、`toecollapse`に対応する、元に戻すツールは今のところ存在しません。  
