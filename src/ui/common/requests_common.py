import os

import requests
import streamlit as st

from common.logger import logger


class Request:
    API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")

    @classmethod
    def get(cls, endpoint: str, **kwargs):
        try:
            r: requests.Response = requests.get(
                url=cls.API_BASE_URL + endpoint, **kwargs
            )
            if r.ok:
                logger.debug(
                    f"{r.url} | {r.request.method} | {r.status_code} {r.reason}"
                )
                return r
            else:
                logger.debug(
                    f"{r.url} | {r.request.method} | {r.status_code} {r.reason}"
                )
        except Exception as e:
            logger.error(e)
            st.error(
                "Hmm..it looks like the API is offline. Try again or check back later."
            )
            st.stop()

    @classmethod
    def post(cls, endpoint: str, **kwargs):
        try:
            r: requests.Response = requests.post(
                url=cls.API_BASE_URL + endpoint, **kwargs
            )
            if r.ok:
                logger.debug(
                    f"{r.url} | {r.request.method} | {r.status_code} {r.reason}"
                )
                return r
            else:
                logger.debug(
                    f"{r.url} | {r.request.method} | {r.status_code} {r.reason}"
                )
        except Exception as e:
            logger.error(e)
            st.error(
                "Hmm..it looks like the API is offline. Try again or check back later."
            )
            st.stop()

    @classmethod
    def delete(cls, endpoint: str, **kwargs):
        try:
            r: requests.Response = requests.delete(
                url=cls.API_BASE_URL + endpoint, **kwargs
            )
            if r.ok:
                logger.debug(
                    f"{r.url} | {r.request.method} | {r.status_code} {r.reason}"
                )
                return r
            else:
                logger.debug(
                    f"{r.url} | {r.request.method} | {r.status_code} {r.reason}"
                )
        except Exception as e:
            logger.error(e)
            st.error(
                "Hmm..it looks like the API is offline. Try again or check back later."
            )
            st.stop()
