# sk-icloud-keychain

iCloud キーチェーンに保存した ed25519 鍵を、各 Mac の Touch ID で解錠して SSH に使うための OpenSSH security key provider です。

- 鍵は iCloud キーチェーンで同期されるので、どの Mac でも**同じ鍵**を Touch ID で使えます。
- サーバからは普通の `sk-ssh-ed25519@openssh.com` 鍵に見えます。`verify-required` を付ければ、Touch ID を通らない署名は受け付けません。
- OpenSSH には手を加えません。`SecurityKeyProvider` で dylib を読み込ませるだけです。YubiKey などの FIDO 鍵と並べて使えます。

`ssh` でログインするたびに、macOS の Touch ID ダイアログが出ます。どの鍵で署名するか（鍵の application 名）が表示されるので、確かめてから指を置きます。

<img src="docs/images/touch-id-dialog-ja.jpg" width="284" alt="Touch ID のダイアログ。「sk-icloud-keychain で次の操作を実行しようとしています: SSH 鍵「ssh:sk-icloud-keychain-dev」で署名」と表示され、右下に雲と鍵穴のアイコンが付いている">

説明文は Mac の言語設定に合わせて日本語か英語で表示され、右下には sk-icloud-keychain のアイコンが付きます。

方式を選んだ経緯は [SSH 鍵保護方式 4 案の比較](https://izawa.github.io/sk-icloud-keychain/SSH%20%E9%8D%B5%E4%BF%9D%E8%AD%B7%E6%96%B9%E5%BC%8F%204%20%E6%A1%88%E3%81%AE%E6%AF%94%E8%BC%83.html)、全体の構成は [構成図](https://izawa.github.io/sk-icloud-keychain/architecture.html)、provider と helper の間の通信は [docs/protocol.md](docs/protocol.md) にまとめてあります。2 つの HTML は GitHub Pages で表示されます（元のファイルは `docs/` にあります）。

## 仕組み

```
ssh ─ ssh-sk-helper ─ libsk-icloud-keychain.dylib ──(パイプ)── sk-icloud-keychain.app
                       （署名不要・OpenSSH が読み込む）          （署名済み・Touch ID・Keychain）
```

- **provider（dylib）**: OpenSSH の sk-api（`sk_enroll` / `sk_sign` / `sk_load_resident_keys`）を実装します。Keychain には触れず、helper を起動して結果を返します。
- **helper（app）**: 鍵の生成と保存、Touch ID での本人確認、署名を担当します。同期するキーチェーン項目を扱うには `keychain-access-groups` の権限が要り、この権限はプロビジョニングプロファイル付きの署名でしか使えません。そのため helper だけは Apple Developer の Team で署名します。

app の中に dylib を同梱しているので、インストールすると次のパスに置かれます。

```
/Applications/sk-icloud-keychain.app/Contents/Frameworks/libsk-icloud-keychain.dylib
```

## 必要なもの

- macOS 14 以降と、Touch ID（内蔵、または Touch ID 付き Magic Keyboard）
- 普段の Apple Account で iCloud キーチェーンがオンになっていること
- 自分でビルドする場合だけ: Xcode と、Apple Developer Program に加入した Apple Account（helper の署名用）。普段の Apple Account と別のアカウントでかまいません
- OpenSSH 8.2 以降。Homebrew の 10.6p1 と、macOS 純正の 10.3 で動作を確認しています

## インストール（Mac ごと）

[Releases](https://github.com/izawa/sk-icloud-keychain/releases/latest) から `sk-icloud-keychain-<版>.dmg` をダウンロードして開き、`sk-icloud-keychain` を `Applications` へドラッグします。

- Developer ID で署名し、Apple の公証を通してあります。Xcode も Apple Developer Program も要りません。
- Mac の登録も要らないので、どの Mac にも同じ DMG から入れられます。
- 鍵は access group `FJYY683YHH.org.izawa.sk-icloud-keychain` に保存されます。どの Mac でも同じ場所なので、iCloud キーチェーンで同期した鍵をそのまま使えます。

入れたら「[鍵を作る](#鍵を作る最初の-1-回だけ)」に進んでください。

### 自分でビルドする

自分の Team で署名した helper を使いたい場合は、ソースからビルドします。**鍵の置き場所は自分の Team の access group になるので、DMG 版で作った鍵とは共有されません。**

1. Xcode に開発用 Apple Account でサインインします（Settings → Apple Accounts）。
2. **自分の Team ID と bundle ID を設定します（必須）。** helper は、あなたの Apple Developer Program の Team で署名する必要があります。設定ファイルの見本をコピーして、2 つの値を書き換えてください。

   ```bash
   cp config.mk.example config.mk
   ```

   | 値 | 書くもの |
   |---|---|
   | `TEAM_ID` | Team ID（英数字 10 文字）。[developer.apple.com/account](https://developer.apple.com/account) の Membership details に表示されます |
   | `BUNDLE_ID` | 自分が持っているドメインを逆にした名前（例: `com.example.sk-icloud-keychain`） |

   `config.mk` は Git の管理外です。リポジトリを Dropbox などで共有していれば、ほかの Mac にもそのまま届きます。ファイルを作らずに `make install TEAM_ID=… BUNDLE_ID=…` と指定することもできます。

   鍵は access group `<TEAM_ID>.<BUNDLE_ID>` に保存されます。**鍵を作ったあとでどちらかを変えると、それまでの鍵は読めなくなります**（サーバへの登録からやり直しになります）。最初に決めた値を使い続けてください。

3. 次を実行します。初回は Mac が端末として登録され、署名用の鍵を使ってよいかの確認ダイアログが出ます。ログインパスワードを入れて「常に許可」を選んでください。

   ```bash
   make install
   ```

自分でビルドした app は、ビルドした Mac 専用の署名になります（開発用プロファイルは登録した Mac でしか起動しません）。他の Mac にはコピーせず、それぞれの Mac で `make install` してください。`make` はビルドの宛先をその Mac にしているので、新しい Mac は自動で Team に登録されます。プロファイルの期限は 1 年なので、1 年ごとに `make install` をやり直します。

ビルド結果は `build/<ホスト名>/` に置かれます。リポジトリを Dropbox などで Mac の間で共有していても、互いのビルドを上書きしません。

helper が起動直後に `killed` になるときは、プロファイルにその Mac が入っていません。`/usr/bin/log show --last 5m --predicate 'eventMessage CONTAINS[c] "sk-icloud-keychain"'` に `Provisioning profile does not allow this device` と出ていれば、`~/Library/Developer/Xcode/UserData/Provisioning Profiles/` を空にしてから `make install` をやり直してください。

## 鍵を作る（最初の 1 回だけ）

```bash
ssh-keygen -t ed25519-sk -O resident -O verify-required \
    -O application=ssh:icloud \
    -w /Applications/sk-icloud-keychain.app/Contents/Frameworks/libsk-icloud-keychain.dylib \
    -f ~/.ssh/id_ed25519_sk_icloud
```

Touch ID を求められます。macOS 純正の `ssh-keygen` などが `Enter PIN for ED25519-SK key:` と聞いてくることがありますが、PIN は使わないので何も入力せずに進めてください。`~/.ssh/id_ed25519_sk_icloud` は鍵ファイルですが、中身は Keychain の項目を指す key handle と公開鍵だけで、秘密鍵は入っていません。

別の Mac では、`~/.ssh` を共有していればそのまま使えます。共有していない場合は、次のコマンドで鍵ファイルを作り直せます（Touch ID は不要です）。

```bash
cd ~/.ssh && ssh-keygen -K -w /Applications/sk-icloud-keychain.app/Contents/Frameworks/libsk-icloud-keychain.dylib
```

## ~/.ssh/config

`SecurityKeyProvider` は、**この鍵を使う Host にだけ**書いてください。`Host *` に書くと、YubiKey などの FIDO 鍵もこの provider に送られて使えなくなります。

```
Host myserver
    HostName myserver.example.com
    IdentityFile ~/.ssh/id_ed25519_sk_icloud
    SecurityKeyProvider /Applications/sk-icloud-keychain.app/Contents/Frameworks/libsk-icloud-keychain.dylib
```

provider のパスはどの Mac でも同じなので、`~/.ssh/config` を Mac の間で共有してもかまいません。

## サーバ側

`~/.ssh/authorized_keys` に公開鍵を 1 行登録します。`verify-required` を付けると、Touch ID を通った署名（UV フラグ付き）だけを受け付けます。

```
verify-required sk-ssh-ed25519@openssh.com AAAA... ssh:icloud
```

Mac を増やしても、サーバ側に鍵を追加する必要はありません。

## 鍵の管理

helper は、コマンドとしても直接使えます。

```bash
H=/Applications/sk-icloud-keychain.app/Contents/MacOS/sk-icloud-keychain
$H list                 # 保存している鍵の一覧（Touch ID 不要）
$H delete <UUID>        # 鍵を削除（Touch ID が必要。iCloud 経由で全 Mac から消えます）
```

`list` の `key_handle` は `skick1:<UUID>` を hex にしたものです。

### 鍵ファイルの中身を確かめる

`~/.ssh/id_ed25519_sk_icloud` は `BEGIN OPENSSH PRIVATE KEY` で始まりますが、security key の鍵ファイルなので秘密鍵は入っていません。入っているのは公開鍵・application・flags・key handle だけです。`tools/sk-key-info` で中身を表示できます（Touch ID は不要です）。

```bash
tools/sk-key-info                              # ~/.ssh の security key ファイルをすべて表示
tools/sk-key-info ~/.ssh/id_ed25519_sk_icloud  # ファイルを指定（.pub を指定してもかまいません）
```

```
~/.ssh/id_ed25519_sk_icloud
  type         sk-ssh-ed25519@openssh.com
  fingerprint  SHA256:pSNJtVwCc0W0gr1vZE15O1hE6viePVgVIo1nbcVx6Dc
  application  ssh:icloud
  flags        0x25 (UP | UV | RESIDENT)
  key handle   skick1:9AE55D73-D732-4AAE-AB5B-4449DA33C764
  comment      izawa sk-icloud-keychain
  provider     sk-icloud-keychain
  keychain     present on this Mac
```

- `flags` の `UV` は、鍵を作るときに `-O verify-required` を付けたことを示します。
- `keychain` は、その鍵がこの Mac の iCloud キーチェーンにあるかどうかです（helper の `list` で確かめます。`--no-keychain` で省略できます）。`NOT on this Mac` なら、まだ同期されていないか、削除されています。
- YubiKey などの鍵ファイルも表示できます。その場合 key handle はバイナリなので hex で表示されます。パスフレーズ付きのファイルは key handle を読めません。
- security key ではない普通の秘密鍵ファイルを指定したときは、種類と指紋だけを表示し、中身は表示しません。

## 安全性と制約

| 観点 | この方式での扱い |
|---|---|
| 秘密鍵を読めるもの | iCloud キーチェーン（E2E 暗号化）と、access group `<TEAM_ID>.<BUNDLE_ID>` に属する app、つまり同じ Team で署名した helper だけ。DMG 版では作者の Team（`FJYY683YHH`）なので、作者がその Team で署名した app を信頼することになります。それを避けたい場合は、自分でビルドしてください |
| 本人確認 | helper が LocalAuthentication で Touch ID を求めます（生体認証のみ、パスワードでの代替なし）。これはソフトウェアでかけるゲートで、Secure Enclave が鍵の使用そのものを強制するわけではありません。生体認証の ACL を付けたキーチェーン項目は同期できないためです |
| helper を呼べるもの | 同じユーザーで動くプロセスなら helper を起動できます。ただし署名のたびに Touch ID が要り、ダイアログには鍵の application（`ssh:…`）が表示されます |
| 鍵の取り違え | 登録時と違う application での署名は拒否します |
| counter | Mac をまたいで単調増加しないので、Unix 時刻を入れています。sshd は既定では counter を見ません |
| 署名の期限 | DMG 版は Developer ID 用のプロファイル（期限 2044 年）と、タイムスタンプ付きの署名なので、入れ直しは要らない見込みです。ただし、署名した証明書が切れた（2027-12-10）あとも helper が起動するかは、まだ確かめていません。自分でビルドした場合は開発用プロファイルの期限が 1 年で、切れると helper が起動しなくなるので、`make install` をやり直します |
| アカウント | 署名した Team の Apple Account を失うと Team ID を引き継げず、鍵を作り直してサーバに登録し直すことになります（DMG 版では作者の Team） |

## 開発

```bash
make            # dylib（テスト用）と helper app をビルド
make test       # 単体テストと、provider が読み込まれるかのテスト（Touch ID 不要）
tests/e2e.sh    # 鍵の作成・署名・検証・-K の通し確認（Touch ID が 2 回）
```

app のアイコンは `helper/App/Icon/AppIcon.svg` が原本です。直したら `helper/App/Icon/make-icns.sh`（`rsvg-convert` が必要）で `AppIcon.icns` を作り直してください。Touch ID のダイアログの右下には、このアイコンが表示されます。アイコンを変えたときは、`helper/SKICloudKeychain.xcodeproj` の `CURRENT_PROJECT_VERSION` も上げてください。macOS はアイコンをバージョンごとにキャッシュするので、同じバージョンのままだと、すでに入れてある Mac では古いアイコンが出続けることがあります。`make install` は入れ直した app を LaunchServices に登録し直しますが、それでも古いアイコン（汎用のグリッド）のままなら、ログアウトしてログインし直すとキャッシュが消えて反映されます。

配布用の DMG は `scripts/release.sh` で作ります（作者向け）。手順は [docs/release.md](docs/release.md) にあります。

`spike/` は、同期するキーチェーン項目に署名が必要かを確かめた最初の実験の記録です。作者の Team ID のまま残してあり、ビルドには使いません。

`SK_ICLOUD_KEYCHAIN_DEBUG=1` を設定すると、provider と helper が標準エラーに経過を出します。`SK_ICLOUD_KEYCHAIN_HELPER` で helper の場所を差し替えられます。

## ライセンス

MIT ライセンスです（[LICENSE](LICENSE)）。

ただし `provider/sk-api.h` は openssh-portable（V_10_6_P1）のファイルで、Google LLC の ISC ライセンス表記をそのまま残しています。
