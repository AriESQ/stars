![Unsupported](https://img.shields.io/badge/development_status-in_progress-green.svg) ![License GPLv3](https://img.shields.io/badge/license-GPLv3-green.svg)

yamss
====

[Y]et [A]nother [M]atrix [S]hell [S]cript

Usage
----

![yamss-gif](yamss.gif)

<pre><code>

NAME
    yamss.sh - matrix like shell script

SYNOPSIS
    ./yamss.sh [OPTION]...

DESCRIPTION
    [Y]et [A]nother [M]atrix [S]hell [S]cript.
    This script shows a matrix like display in terminal.

OPTIONS
    -a
            This option sets asynchronous mode.
            Default is disabled

    -c [number]
            This option sets the characters used for display.
            Different characters listed in chart below.
            Default is standard (1).

    -d
            This option runs everything in default settings.
            This should be run by itself.

    -h [number]
            This option sets the highlite color according to
            the color chart below.
            Default is 37 (white)

    -m [number]
            This option sets the main color according to
            the color chart below.
            Default is 34 (blue)

    -q [letter]
            This option specifies what letter to use to quit
            out of this script instead of using ctrl + c.
            Default is q

    -r
            This option specifies rainbow road mode.
            All main and highlite colors will be random from
            the color chart below.
            Default is disabled

    -s [number]
            This option sets drop speed.
            Range is from 1 (fastest ) to 10 ( slowest )
            Default is 1

CHARACTER CHART
    Option [1]:
        Standard: 123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]
                  ^_abcdefghijklmnopqrstuvwxyz{|}

    Option [2]:
           Kanji: ⼀⼁⼂⼃⼄⼅⼆⼇⼈⼉⼊⼋⼌⼍⼎⼏⼐⼑⼒⼓⼔⼕
                  ⼖⼗⼘⼙⼚⼛⼜⼝⼞⼟⼠⼡⼢⼣⼤⼥⼦⼧⼨⼩⼪⼫
                  ⼬⼭⼮⼯⼰⼱⼲⼳⼴⼵⼶⼷⼸⼹⼺⼻⼼⼽⼾⼿⽀⽁
                  ⽂⽃⽄⽅⽆⽇⽈⽉⽊⽋⽌⽍⽎⽏⽐⽑⽒⽓⽔⽕⽖⽗
                  ⽘⽙⽚⽛⽜⽝⽞⽟⽠⽡⽢⽣⽤⽥⽦⽧⽨⽩⽪⽫⽬⽭
                  ⽮⽯⽰⽱⽲⽳⽴⽵⽶⽷⽸⽹⽺⽻⽼⽽⽾⽿⾀⾁⾂⾃
                  ⾄⾅⾆⾇⾈⾉⾊⾋⾌⾍⾎⾏⾐⾑⾒⾓⾔⾕⾖⾗⾘⾙
                  ⾚⾛⾜⾝⾞⾟⾠⾡⾢⾣⾤⾥⾦⾧⾨⾩⾪⾫⾬⾭⾮⾯
                  ⾰⾱⾲⾳⾴⾵⾶⾷⾸⾹⾺⾻⾼⾽⾾⾿⿀⿁⿂⿃⿄⿅
                  ⿆⿇⿈⿉⿊⿋⿌⿍⿎⿏⿐⿑⿒⿓⿔⿕

    Option [3]:
            Misc: ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍ
                  ÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øù
                  úûüýþÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥ
                  ĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐő
                  ŒœŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽ
                  žſƀƁƂƃƄƅƆƇƈƉƊƋƌƍƎƏƐƑƒƓƔƕƖƗƘƙƚƛƜƝƞƟƠơƢƣƤƥƦƧƨƩ
                  ƪƫƬƭƮƯưƱƲƳƴƵƶƷƸƹƺƻƼƽƾƿǀǁǂǃǄǅǆǇǈǉǊǋǌǍǎǏǐǑǒǓǔǕ
                  ǖǗǘǙǚǛǜǝǞǟǠǡǢǣǤǥǦǧǨǩǪǫǬǭǮǯǰǱǲǳǴǵǶǷǸǹǺǻǼǽǾǿȀȁ
                  ȂȃȄȅȆȇȈȉȊȋȌȍȎȏȐȑȒȓȔȕȖȗȘșȚțȜȝȞȟȠȡȢȣȤȥȦȧȨȩȪȫȬȭ
                  ȮȯȰȱȲȳȴȵȶȷȸȹȺȻȼȽȾȿɀɁɂɃɄɅɆɇɈɉɊɋɌɍɎɏɐɑɒɓɔɕɖɗ%

    Option [4]:
          Blocks: ░▒▓

    Option [5]:
          Lines: |


COLOR CHART
    30      Black
    31      Red
    32      Green
    33      Yellow
    34      Blue
    35      Magenta
    36      Cyan
    37      White

</code></pre>

Requirements
----

- Bash (https://www.gnu.org/software/bash/)
- GNU Awk (https://www.gnu.org/software/gawk/)
- GNU BC (https://www.gnu.org/software/bc/)


License and Author
----

Author:: Cesar Bodden (cesar@pissedoffadmins.com)

Copyright:: 2016, Pissedoffadmins.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
