FROM kivy/python-for-android:latest

RUN cd /tmp  && \
    git clone --branch android https://github.com/g-revilla/watermark.git && \
    pip install --no-cache-dir buildozer cython

WORKDIR /tmp/watermark/build

CMD ["bash"]