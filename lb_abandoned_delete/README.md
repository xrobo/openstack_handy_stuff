Скрипт удаления оставшихся балансировщиков
==========================================

## Описание проблемы

После удаления кластера Kubernetes остается его ingress-балансировщик.

## Логика скрипта

Название балансировщика содержит UUID кластера (cluster_uuid). После сопоставления данных балансировщиков и кластеров проекта, скрипт предлагает удалить те балансировщики, для которых не нашлось cluster_uuid среди кластеров.

## Требование и запуск скрипта

Скрипт написан на bash'e и использует утилиту ```openstack```.

В режиме доступа к проекту OpenStack (заданы необходимые переменные окружения OS_*):
1. Запуск скрипта без параметров:

```lb_abandoned_delete.sh```

Если найдутся оставшиеся после удаления кластеров балансировщики, то скрипт выдаст запрос на подтверждения их удаления.

2. Запуск скрипта с параметром 'ls' только выведет результат сопоставления данных:

```lb_abandoned_delete.sh ls```