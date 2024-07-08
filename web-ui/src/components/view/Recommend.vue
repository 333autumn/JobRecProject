<template>
	<h1>职位推荐</h1>
	<el-card v-for="data in list" style="margin-bottom:20px;" shadow="hover">
		<el-row>
			<el-col :span="20">
				<el-descriptions :title="data.name">
					<el-descriptions-item label="工作名称">{{data.name}}</el-descriptions-item>
					<el-descriptions-item label="所属公司">{{data.companyname}}</el-descriptions-item>
					<el-descriptions-item label="工作性质">{{data.property}}</el-descriptions-item>
					<el-descriptions-item label="产业名称">{{data.industryname}}</el-descriptions-item>
					<el-descriptions-item label="工作地址">{{data.workcity}}</el-descriptions-item>
				</el-descriptions>
			</el-col>
			<el-col :span="4">
				<el-button type="primary" style="margin-top: 30px;">简历投递</el-button>
			</el-col>
		</el-row>
	</el-card>
</template>

<script>
	export default {

		name: 'Recommend',
		data() {
			return {
				//列表数据
				list: [],
			};
		},
		props: {
			userinfo: {
				type: Object,
				required: true,
			},
		},
		methods: {

		},
		created() {
			this.$http.get(this.$api.recommend).then(response => {
				this.list = response.data.data;
			});
		},
	}
</script>

<style>

</style>


<!-- <template>
	<List :dataurl="$api.recommend" :listType="0"></List>
</template>

<script>
	import List from '../utils/List.vue'
	export default {

		name: 'Recommend',
		data() {
			return {

			};
		},
		props: {
			userinfo: {
				type: Object,
				required: true,
			},
		},
		methods: {


		},
		components: {
			List
		}
	}
</script>

<style>

</style> -->