; (function ($, window, document, undefined) {

	var onMobile = 'ontouchstart' in window,
		eStart = onMobile ? 'touchstart' : 'mousedown',
		eMove = onMobile ? 'touchmove' : 'mousemove',
		eCancel = onMobile ? 'touchcancel' : 'mouseup',
		hackPrefixes = ['webkit', 'moz', 'ms', 'o'],
		hackHiddenProperty = getHackHidden();

	$.fn.initAudioPlayer = function () {
		// 遍历处理audio
		this.each(function () {
			if ($(this).prop('tagName').toLowerCase() !== 'audio') {
				return;
			}

			var $this = $(this),
				file = $this.attr('src'),
				isSupport = false;

			if (canFilePlay(file)) {
				isSupport = true;
			} else {
				$this.find('source').each(function () {
					if (canFilePlay($(this).attr('src'))) {
						isSupport = true;
						return false;
					}
				});
			}

			if (!isSupport) {
				return;
			}

			// 添加播放器盒子
			var $player = $('<div class="ppq-audio-player">' + $('<div>').append($this.eq(0).clone()).html() + '<div class="play-pause-btn"><a href="javascript: void(0);" class="play-pause-icon" id="playButton"></a></div></div>'),
				audioEle = $player.find('audio')[0];

			$player.find('audio').addClass('audio-hidden');
			$player.append('<div class="player-time player-time-current"></div>\
				<div class="player-time player-time-duration"></div>\
				<div class="player-bar">\
					<div class="player-bar-loaded"></div>\
					<div class="player-bar-played"></div>\
				</div>');

			var $bar = $player.find('.player-bar'),
				$played = $player.find('.player-bar-played'),
				$loaded = $player.find('.player-bar-loaded'),
				$current = $player.find('.player-time-current'),
				$duration = $player.find('.player-time-duration');

			$current.html('00:00');
			$duration.html('&hellip;');

			initAudioEvents();
			bindPageEvents();
			$this.replaceWith($player);

			function initAudioEvents() {
				// 监听loadeddata，渲染进度条和时间
				audioEle.addEventListener('loadeddata', function () {
					var loadTimer = setInterval(function () {
						if (audioEle.buffered.length < 1) {
							return true;
						}
						$loaded.width((audioEle.buffered.end(0) / audioEle.duration) * 100 + '%');
						if (Math.floor(audioEle.buffered.end(0)) >= Math.floor(audioEle.duration)) {
							clearInterval(loadTimer);
						}
					}, 100);
					$duration.html($.isNumeric(audioEle.duration) ? convertTimeStr(audioEle.duration) : '&hellip;');
				});

				// 监听timeupdate，更新时间和进度条
				audioEle.addEventListener('timeupdate', function () {
					$current.html(convertTimeStr(audioEle.currentTime));
					$played.width((audioEle.currentTime / audioEle.duration) * 100 + '%');
				});

				// 监听ended，播放完恢复暂停状态
				audioEle.addEventListener('ended', function () {
					$player.removeClass('player-playing').addClass('player-paused');
				});
			}

			function bindPageEvents() {
				// 监听进度条touch，更新进度条和播放进度
				$bar.on(eStart, function (e) {
					audioEle.currentTime = getCurrentTime(e);
					$bar.on(eMove, function (e) {
						audioEle.currentTime = getCurrentTime(e);
					});
				}).on(eCancel, function () {
					$bar.unbind(eMove);
				});

				// 监听播放暂停按钮click
				$player.find('.play-pause-btn').on('click', function () {
					if ($player.hasClass('player-playing')) {
						$player.removeClass('player-playing').addClass('player-paused');
						audioEle.pause();
					} else {
						$player.addClass('player-playing').removeClass('player-paused');
						audioEle.play();
					}
					return false;
				});
			}

			function getCurrentTime(e) {
				var et = onMobile ? e.originalEvent.touches[0] : e;
				return Math.round((audioEle.duration * (et.pageX - $bar.offset().left)) / $bar.width());
			}

			if (hackHiddenProperty) {
				var evtname = hackHiddenProperty.replace(/[H|h]idden/, '') + 'visibilitychange';
				document.addEventListener(evtname, function () {
					if (isHidden() || getHackVisibilityState() === 'hidden') {
						$player.removeClass('player-playing').addClass('player-paused');
						audioEle.pause();
					}
				}, false);
			}

			window.addEventListener('beforeunload', function () {
				$player.removeClass('player-playing').addClass('player-paused');
				audioEle.pause();
			}, false);
		});
		return this;
	}

	// 秒转为时间字符串
	function convertTimeStr(secs) {
		var m = Math.floor(secs / 60),
			s = Math.floor(secs - m * 60);
		return (m < 10 ? '0' + m : m) + ':' + (s < 10 ? '0' + s : s);
	}

	// 判断文件能不能播放
	function canFilePlay(file) {
		if (!file) {
			return false;
		}
		var media = document.createElement('audio');
		if (typeof media.canPlayType !== 'function') {
			return false;
		}

		var res = media.canPlayType('audio/' + file.split('.').pop().toLowerCase());
		return res === 'probably' || res === 'maybe';
	}

	function getHackHidden() {
		if ('hidden' in document) {
			return 'hidden';
		}
		for (var i = 0; i < hackPrefixes.length; i++) {
			if ((hackPrefixes[i] + 'Hidden') in document) {
				return hackPrefixes[i] + 'Hidden';
			}
		}
		return null;
	}

	function getHackVisibilityState() {
		if ('visibilityState' in document) {
			return 'visibilityState';
		}
		for (var i = 0; i < hackPrefixes.length; i++) {
			if ((hackPrefixes[i] + 'VisibilityState') in document) {
				return hackPrefixes[i] + 'VisibilityState';
			}
		}
		return null;
	}

	function isHidden() {
		var hide = getHackHidden();
		if (!hide) {
			return false;
		}

		return document[hide];
	}
})(jQuery, window, document);