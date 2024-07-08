<template>
	<!-- 统计图表 -->
	<section class="mainbox" style="flex-direction: column;margin-top: 40px;">
		<div class="charts">
			<div class="column leftchart">
				<div class="panel pie">
					<h1>就业类型分布</h1>
					<div class="chart" ref="left3"></div>
					<div class="panel-footer"></div>
				</div>
			</div>
			<div class="column rightchart">
				<div class="panel pie2">
					<h1>各地点岗位数量占比</h1>
					<div class="chart" ref="right3"></div>
					<div class="panel-footer"></div>
				</div>
			</div>
		</div>
	</section>
</template>

<script setup>
	import {
		markRaw
	} from 'vue'
</script>

<script>
	export default {
		name: 'BigView',
		created() {
			let script = document.createElement('script');
			script.type = 'text/javascript';
			script.src = '/assets/js/flexible.js';
			document.body.appendChild(script);
			let link = document.createElement('link');
			link.rel = 'stylesheet';
			link.href = '/assets/css/charts.css';
			document.body.appendChild(link);
			this.getinfo()
			window.setInterval(this.getinfo, 60000)
		},
		mounted() {
			this.charts()
		},
		data() {
			return {
				methods: false,
				t: null,
				resize: null,
				mapchart: null,
				left3: null,
				right3: null,
				info: {
					total: [0],
					count: [0],
					uncollected: [0]
				},
				right3_info: {},
				left3_info: {},
			}
		},
		methods: {
			getinfo() {
				//首先读取浏览器缓存
				this.info = JSON.parse(localStorage.getItem('bigdata_info'));
				//缓存中有数据直接返回
				if (this.info != null) return;
				//发送请求
				this.$http.get(this.$api.jobs + 'bigdata_info/', {
						headers: {
							'Content-Type': 'application/json',
						}
					})
					.then(response => {
						this.info = response.data.data;
						//保存信息到浏览器缓存中
						window.localStorage.setItem('bigdata_info', JSON.stringify(this.info));
					})
					.catch(error => {
						console.error(error)
						this.$message({
							type: 'error',
							text: '加载失败'
						})
					});
			},
			async charts() {
				this.$nextTick(() => {
					this.left3 = markRaw(this.$echarts.init(this.$refs.left3));
					this.right3 = markRaw(this.$echarts.init(this.$refs.right3));
					this.Left3()
					this.Right3()
				});
			},
			Filter(e) {
				if (!e.target.classList.contains('filter_active')) {
					if (e.target.previousElementSibling) {
						e.target.previousElementSibling.classList.remove('filter_active')
						e.target.classList.add('filter_active')
					} else {
						e.target.nextElementSibling.classList.remove('filter_active')
						e.target.classList.add('filter_active')
					}
					this.methods = !this.methods
					this.getinfo()
					this.Left3()
					this.Right3()
				}
			},
			async Right3() {
				//首先读取浏览器缓存
				this.right3_info = JSON.parse(localStorage.getItem('workcity_info'));
				if (this.right3_info == null) {
					await this.$http.get(this.$api.jobs + 'workcity_info/', {
							headers: {
								'Content-Type': 'application/json',
							}
						})
						.then(response => {
							this.right3_info = response.data.data;
							//保存信息到浏览器缓存中
							window.localStorage.setItem('workcity_info', JSON.stringify(this.right3_info));
						})
						.catch(error => {
							console.error(error)
						});
				}
				var option = {
					color: ['#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff'],
					tooltip: {
						trigger: 'item',
						formatter: '{a} <br/>{b} : {c} ({d}%)'
					},
					legend: {
						bottom: 0,
						itemWidth: 10,
						itemHeight: 10,
						textStyle: {
							color: "rgba(0, 0, 0, 0.5)",
							fontSize: 10
						}
					},
					series: [{
						name: '地点分布',
						type: 'pie',
						radius: ["10%", "60%"],
						center: ['50%', '40%'],
						// 半径模式  area面积模式
						roseType: 'radius',
						// 图形的文字标签
						label: {
							fontsize: 10
						},
						// 引导线调整
						labelLine: {
							// 连接扇形图线长(斜线)
							length: 8,
							// 连接文字线长(横线)
							length2: 10
						},
						data: this.right3_info
					}]
				};
				this.right3.setOption(option)
			},
			async Left3() {
				//首先读取浏览器缓存
				this.left3_info = JSON.parse(localStorage.getItem('worktype_info'));
				if (this.left3_info == null) {
					await this.$http.get(this.$api.jobs + 'worktype_info/', {
							headers: {
								'Content-Type': 'application/json',
							}
						})
						.then(response => {
							this.left3_info = response.data.data;
							//保存信息到浏览器缓存中
							window.localStorage.setItem('worktype_info', JSON.stringify(this.left3_info));
						})
						.catch(error => {
							console.error(error)
						});
				};
				var option = {
					// color: ["#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6"],
					tooltip: {
						trigger: 'item',
						formatter: '{a} <br/>{b}: {c} ({d}%)'
					},
					legend: {
						// 垂直居中,默认水平居中
						// orient: 'vertical',
						bottom: 0,
						// left: 10,
						// 小图标的宽度和高度
						itemWidth: 10,
						itemHeight: 10,
						// 修改图例组件的文字为 12px
						textStyle: {
							color: "rgba(0, 0, 0, 0.5)",
							fontSize: "10"
						}
					},
					series: [{
						name: '类型分布',
						type: 'pie',
						// 设置饼形图在容器中的位置
						center: ["50%", "42%"],
						// 修改饼形图大小，第一个为内圆半径，第二个为外圆半径
						radius: ['40%', '60%'],
						avoidLabelOverlap: false,
						// 图形上的文字
						label: {
							show: false,
							position: 'center'
						},
						// 链接文字和图形的线
						labelLine: {
							show: false
						},
						data: this.left3_info
					}]
				}
				this.left3.setOption(option)
			},
		},
	}
</script>

<style lang="less" scoped>
	.filter {
		display: flex;
		flex-direction: row;
		color: white;
		width: 70px;
		font-size: 15px;
		justify-content: space-between;
	}

	.filter_active {
		border-bottom: 1.5px gray solid;

	}

	.filter>div {
		cursor: pointer;
	}

	header {
		padding: 20px 15px;
		height: 120px;
	}

	.map {
		flex: 1;
	}

	.title {
		text-align: center;
		font-size: 40px;
		margin: 0;
		line-height: 40px;
	}

	.timer {

		font-size: 15px;
		text-align: right;
		color: rgba(255, 255, 255, 0.87);
	}

	.no ul {
		margin: 0;
		padding: 0;
	}

	.column {
		display: flex;
		flex-direction: column;

	}


	.mainbox .panel {
		height: 400px;
	}

	.mainbox .panel .chart {
		height: 80%;
	}

	.no {
		flex: unset;
	}

	.leftchart,
	.rightchart {
		width: 50%;
	}

	.centerchart {
		flex: unset
	}

	.chart {
		margin-bottom: 20px;
	}

	.charts {
		display: flex;
		flex-direction: row;
		flex: 1
	}

	@media only screen and (max-width: 990px) {
		.mainbox .panel {
			height: 300px;
		}

		.mainbox {
			width: 100%;
			height: 100%;
		}

		.mainbox .panel h2 {
			margin-top: 15px;
		}

		.map {
			display: none;
		}

		.chart {
			height: 250px !important;
			width: 95%;
		}

		.leftchart,
		.rightchart {
			width: 100%;
		}

		.timer {
			text-align: center;
		}

		header {
			padding: 15px 15px;
			height: 100px;

		}

		.title {
			text-align: center;
			font-size: 25px;
			margin-bottom: 15px;
			line-height: 20px;
		}

		.charts {
			flex-direction: column;
		}
	}
</style>