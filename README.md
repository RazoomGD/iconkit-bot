# GD Icon kit bot

Ссылка на бота:
- https://t.me/gd_icon_kit_bot

## Предисловие
Итак, это бот, который сделан для удобной работы с ГД-иконками
через телеграм. Когда вы впервые ему пишите вам присваивается дефолтный набор
иконок и цветов. Вы можете их просматривать, изменять и скачивать, пользуясь командами бота, а также инлайн-интерфейсом.

## Команды
- `/iconkit` - бот покажет ваш набор иконок
- `/choose` - бот предложит поменять иконки вручную или импортировать их с серверов GD по нику игрока
  - В ручном режиме вам будет предложено изменить персонажа, цвета, а также выставить glow. При выборе можно использовать [инлайн-интерфейс](#инлайн-команды).
  - В режиме импорта, от вас требуется только ввести ник игрока в Geometry Dash. Бот сделает запрос на сервера ГД (boomlings.com) и получит с них 
    иконки игрока с указанным ником. Вам будет предложено выбрать их или оставить прежние.
- `/cube`, `/ship`, `/ball`, `/ufo`, `/wave`, `/robot`, `/spider`, `/swing`, `/jetpack` - 
   эти команды используются для просмотра соответствующих иконок по отдельности. Под отправленной картинкой с иконкой будет кнопка для 
   получения png-файла с иконкой, который может быть нужен, если вы хотите получить картинку с прозрачным фоном и без потери качества
- `/support` - вы можете оставить фитбэк или сообщить о проблеме или задать вопрос
- `/about` - вы можете получить немного информации об этом боте
- `/help` - вы можете посмотреть список команд 
- `/cancel` - используется в некоторых других командах 


## Инлайн-команды

Инлайн-команды - это по сути использование строки ввода сообщения как строки поиска. Инлайн команды начинаются с "@" + "имя_бота". В этом боте доступны следующие инлайн-команды

- `@gd_icon_kit_bot cube`
- `@gd_icon_kit_bot ship`
- `@gd_icon_kit_bot ball`
- `@gd_icon_kit_bot ufo`
- `@gd_icon_kit_bot wave`
- `@gd_icon_kit_bot robot`
- `@gd_icon_kit_bot spider`
- `@gd_icon_kit_bot swing`
- `@gd_icon_kit_bot jetpack`
- `@gd_icon_kit_bot color`

Бот предложит использовать одну из этих команд при выборе соответствующей иконки.
При вводе команды в строку для сообщения открывается окно для выбора соответсвующей иконки или цвета. После выбора, в чат отправиться только id выбранной иконки
(который как раз нужен при выборе иконок командой `/choose`)

## Как устроен исходный код

Проект поделен на 3 большие части:
- часть в директории [icons](icons) отвечает за [сборку](icons/icon.py) иконок из [спрайтов](icons/textures) (все файлы я взял из ресурсов GD).
В этой же части есть дополнительные [функции](icons/icon_utils.py) для работы с иконками, которые используются в боте для их представления. Тут же 
и функции для импорта иконок с серверов ГД.
- часть в директории [telegram](telegram) отвечает за все что связано с телеграмом: все обработчики команд лежат в директории [routers](telegram/routers).
- последнее - в директории [db](db) лежат файлы связанные с работой с базой данных (ладно, это просто json файл - я считаю, для небольшого телеграм бота этого вполне достаточно)

Есть также особенность, связанная с инлайн-режимом: все файлы используемые в инлайн-режиме были заранее сгенерированы и 
выложены на github.io. И бот получает к ним доступ по url (я пробовал разные способы реализовать инлайн режим и способ с доступом по url показал себя лучше других)
Если что, используемые генераторы и автосгенерированная конфигурация лежат в директории [pre_built](telegram/pre_built), а файлы выложены [здесь](https://github.com/RazoomGD/RazoomGD.github.io/tree/main/icon_kit_bot/preloaded)

Если вдруг вы решите запустить проект, то вам понадобится также установить конфигурацию бота в файле [config.py](config.py) или в переменных окружения:
- `BOT_TOKEN` - токен телеграм бота
- `SUPPORT_GROUP_ID` - когда пользователь использует команду `/support`, сообщения, которые он оставляет, будут перенаправляться в этот чат - приватный чат разработчика (сам бот тоже должен быть в этом чате). Чтобы дать пользователю ответ, надо ответить на сообщение из этого чата
- `PROJECT_ROOT` - корневая директория проекта
- `TELEGRAM_PREMADE_COLORS_FOLDER_URL` - url директории, куда выложены автосгенерированные цвета для показа в инлайн режиме
- `TELEGRAM_PREMADE_ICONS_FOLDER_URL` - url директории, куда выложены автосгенерированные иконки для показа в инлайн режиме
- также с помощью BotFather нужно будет установить разрешение на использование инлайн-режима для вашего бота

## Итог

Я потратил неделю на написание этого проекта. Это мой первый бот, да и главная цель создания этого бота была попробовать себя в этом, получить опыт. Если честно, это было очень интересно. 

Были и сложности. Сложнее всего было реализовать сборку иконок из файлов текстур (особенно с роботом и пауком), а также инлайн-режим. Но кажется, в итоге у меня получился неплохой код (по крайней мере так я его оцениваю).

Почти везде он хорошо разделен по файлам и функциям, а у каждого модуля своя независимая область ответственности. Я получил хороший опыт, работая над этим проектом. Главное, что я понял - это
что надо уделять больше времени планированию структуры проекта и отдельных модулей - из-за того что я этого не сделал, мне пришлось переписать пару сотен строк кода. 2 раза... Но кажется, урок усвоен.

И в итоге я доволен тем, что у меня получилось. (на самом деле это может быть просто 1200 строк ужасного кода - кто знает 🤷‍♂️)