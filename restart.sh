#!/bin/bash
sleep 150
docker stop fastapi_load_balancer_web_2 &
sleep 100
docker start fastapi_load_balancer_web_2

