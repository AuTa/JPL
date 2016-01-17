#coding: utf-8

from flask import Blueprint, render_template, redirect, url_for, request, flash, session

kana = Blueprint('kana', __name__)


@kana.route('/')
def index():
    pass

