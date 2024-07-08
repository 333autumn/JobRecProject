<template>
	<!-- 搜索框 -->
	<el-row style="width: 400px;margin-top: 20px;margin-bottom: 20px;">
		<el-col :span="20">
			<el-input placeholder="请输入搜索关键词" v-model="key" clearable></el-input>
		</el-col>
		<el-col :span="4">
			<el-button type="primary" @click="search">
				搜索
			</el-button>
		</el-col>
	</el-row>
	<!-- 根据条件检索人才 -->
	<el-row>
		<el-form-item label="工作经验">
			<el-select v-model="Q.workingexpCode" class="m-2" placeholder="工作经验">
				<el-option v-for="item in this.$baseData.workExpType" :key="item.name" :label="item.name"
					:value="item.code" />
			</el-select>
		</el-form-item>
		<el-form-item label="学历" style="margin-left: 10px;">
			<el-select v-model="Q.eduHighestLevel" class="m-2" placeholder="学历">
				<el-option v-for="item in this.$baseData.educationType" :key="item.name" :label="item.name"
					:value="item.code" />
			</el-select>
		</el-form-item>
	</el-row>
	<!-- 人才列表 -->
	<el-card v-for="data in list" style="margin-bottom:20px;" shadow="hover">
		<el-row>
			<el-col :span="20">
				<el-descriptions :title="data.user.name">
					<el-descriptions-item label="教育水平">{{data.eduHighestLevelTranslation}}</el-descriptions-item>
					<el-descriptions-item label="工作经验">{{data.workingexp}}</el-descriptions-item>
					<el-descriptions-item label="期望工作类型">{{data.worktype}}</el-descriptions-item>
					<el-descriptions-item label="技能标签">
						<el-tag size="small">{{data.skilllabel}}</el-tag>
					</el-descriptions-item>
					<el-descriptions-item label="期望最低工资">
						{{data.preferredSalaryMin}}
					</el-descriptions-item>
				</el-descriptions>
			</el-col>
			<el-col :span="4">
				<el-button type="primary" style="margin-top: 30px;">联系他/她</el-button>
			</el-col>
		</el-row>
	</el-card>
</template>

<script>
	export default {
		name: 'Search',
		data() {
			return {
				//搜索关键词
				key: "",
				//列表数据
				list: [],
				citysub: [{
					'code': null,
					'name': null
				}],
				//检索条件
				Q: {
					city: '',
					citydistrict: '',
					workingexpCode: '-1',
					eduHighestLevel: '-1',
					propertycode: '0',
					subjobtypelevel: '-1',
					worktypeCode: '-1',
					salarytype: '0000,9999999',
					companysize: '不限'
				}
			}
		},
		created() {
			//默认获取全部人才数据
			this.$http.get(this.$api.resumeList, {
				headers: {
					'Content-Type': 'application/json',
				}
			}).then(response => {
				this.list = response.data.data;
			})
		},
		methods: {
			//搜索人才
			search() {
				//根据条件查询
				const data = {
					'workingexpCode': this.Q.workingexpCode,
					'eduHighestLevel': this.Q.eduHighestLevel,
					'key': this.key,
				};
				//根据关键词查询
				this.$http.post(this.$api.searchPeople, data).then(response => {
					this.list = response.data.data;
					this.key = "";
				});
			},
			//清空地址
			clearaddress() {
				this.citysub = []
				this.$baseData.allCity.forEach(element => {
					if (element.code == this.Q.city) {
						this.citysub = element.sublist
					}
				})
				this.Q.citydistrict = ''
			},
		}
	}
</script>

<style scoped>
	.el-select {
		width: 100px;

	}

	.el-input__wrapper>* {
		height: 100% !important;
	}

	.select-input>div>div {
		margin-right: 5px;
	}

	.el-select {
		min-width: 75px !important;

	}

	.el-button {
		width: 75px;
		border: 0 !important;
		box-shadow: none !important;
		border-radius: 0 10px 10px 0;
		color: none;
	}

	.el-input__inner {
		border: 0 !important;
		box-shadow: none;
		background-color: none;

	}

	.search-input {
		display: flex;
		flex-direction: row;
		flex-wrap: nowrap;
		margin-bottom: 15px;
		border: 1px var(--el-menu-border-color) solid;
		border-radius: 10px;

	}

	.el-pagination {
		justify-content: center;
		margin-top: 15px;
	}

	.jobs {
		width: 400px;
		padding: 16px 0 16px 24px;
	}

	.jobs * {
		font-size: 18px;
	}

	.jobs>p>* {
		margin-right: 15px;
	}

	.query {
		margin-bottom: 15px;
		background-color: white;
		padding: 20px 15px;
		border-radius: 15px;
	}

	.companys,
	.companys2 {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 16px 24px 16px 10px;
		width: 250px;
	}

	.list-items-footer * {
		font-size: 13px !important;
		font-weight: 400 !important;
		color: #666 !important;
		line-height: 18px !important;
		word-break: break-word !important;
		-ms-word-break: break-all !important;
		overflow: hidden !important;
		text-overflow: ellipsis !important;
		white-space: nowrap;
		/* 禁止文本换行 */
		overflow: hidden;
		/* 超出部分隐藏 */
		text-overflow: ellipsis;
	}

	.list-items-footer {
		-webkit-text-size-adjust: 100%;
		font-family: Helvetica Neue, Helvetica, Arial, PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif;
		font-size: 14px;
		line-height: 1.5;
		color: #414a60;
		-webkit-font-smoothing: antialiased;
		list-style: none;
		box-sizing: border-box;
		-webkit-tap-highlight-color: transparent;
		margin: 0;
		padding: 15px 24px;
		background: linear-gradient(90deg, #f5fcfc, #fcfbfa);
		border-radius: 0 0 12px 12px;
		cursor: pointer;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.list-items-body {
		display: flex;
		justify-content: space-between;
		align-items: center;
		-webkit-text-size-adjust: 100%;
		font-family: Helvetica Neue, Helvetica, Arial, PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif;
		font-size: 14px;
		line-height: 1.5;
		color: #414a60;
		-webkit-font-smoothing: antialiased;
		list-style: none;
		cursor: pointer;
		box-sizing: border-box;
		-webkit-tap-highlight-color: transparent;
		margin: 0;
		padding: 0;
	}

	a:hover {
		color: orange;
	}

	.list-items:hover {
		box-shadow: 0 10px 10px 0 rgba(0, 0, 0, .12)
	}

	.list-items {
		margin-bottom: 15px;
		-webkit-text-size-adjust: 100%;
		font-family: Helvetica Neue, Helvetica, Arial, PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif;
		font-size: 14px;
		line-height: 1.5;
		color: #414a60;
		-webkit-font-smoothing: antialiased;
		box-sizing: border-box;
		-webkit-tap-highlight-color: transparent;
		padding: 0;
		list-style: none;
		position: relative;
		width: 100%;
		background: #fff;
		border-radius: 12px;
		transition: all .2s linear;
		cursor: pointer;
	}

	@media screen and (max-width: 1000px) {

		.companys {
			display: none !important;
		}

		.welfaretaglist {
			display: none;
		}
	}
</style>