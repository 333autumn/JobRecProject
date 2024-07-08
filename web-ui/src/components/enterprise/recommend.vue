<template>
	<h3>智能推荐</h3>
	<div style="margin-top: 20px;" shadow="always" v-loading="loading">
		<el-card v-for="data in list" style="margin-bottom:20px;" shadow="hover">
			<el-row>
				<el-col :span="20">
					<el-descriptions :title="data.realname">
						<el-descriptions-item label="性别">{{data.sex}}</el-descriptions-item>
						<el-descriptions-item label="年龄">{{data.age}}</el-descriptions-item>
						<el-descriptions-item label="学历">{{data.xlmc}}</el-descriptions-item>
						<el-descriptions-item label="学习形式">{{data.xxxsmc}}</el-descriptions-item>
						<el-descriptions-item label="专业">{{data.zyfx}}</el-descriptions-item>
						<el-descriptions-item label="期望工作类型">{{data.gzzwlbmc}}</el-descriptions-item>
						<!-- <el-descriptions-item label="技能标签">
							<el-tag size="small">{{data.skilllabel}}</el-tag>
						</el-descriptions-item> -->
						<!-- <el-descriptions-item label="期望最低工资">
							{{data.preferredSalaryMin}}
						</el-descriptions-item> -->
					</el-descriptions>
				</el-col>
				<el-col :span="4">
					<el-button type="primary" style="margin-top: 30px;">联系他/她</el-button>
				</el-col>
			</el-row>
		</el-card>
	</div>
</template>

<script>
	export default {
		name: 'recommend',
		data() {
			return {
				activeName: "first",
				//列表数据
				list: [],
				//加载中
				loading: true,
			};
		},
		created() {
			this.$http.get(this.$api.recommendPeople, {
				headers: {
					'Content-Type': 'application/json',
				}
			}).then(response => {
				// console.log(response.data.data);
				this.list = response.data.data;
				this.loading = false;
			})
		},
		methods: {},
	}
</script>

<style scoped>
</style>