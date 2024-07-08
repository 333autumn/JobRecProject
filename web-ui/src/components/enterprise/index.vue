<template>
	<el-container>
		<!-- 左侧区域 -->
		<el-aside width="200px">
			<el-menu active-text-color="#ffd04b" background-color="#324157" class="el-menu-vertical-demo"
				default-active="/enterprise/home" text-color="#fff" @open="handleOpen" @close="handleClose"
				:router="true">
				<div style="text-align: center;color: white;">
					<h2 style="margin-top: 20px;margin-bottom: 20px;">企业端</h2>
				</div>
				<el-menu-item index="/enterprise/home">
					<el-icon><icon-menu /></el-icon>
					<span>首页</span>
				</el-menu-item>
				<el-menu-item index="/enterprise/center">
					<el-icon><icon-menu /></el-icon>
					<span>职位管理</span>
				</el-menu-item>
				<el-menu-item index="/enterprise/recommend">
					<el-icon><icon-menu /></el-icon>
					<span>推荐人才</span>
				</el-menu-item>
				<el-menu-item index="/enterprise/search">
					<el-icon><icon-menu /></el-icon>
					<span>搜索人才</span>
				</el-menu-item>
				<!-- <el-menu-item index="/enterprise/test">
					<el-icon><icon-menu /></el-icon>
					<span>测试</span>
				</el-menu-item> -->
			</el-menu>
		</el-aside>
		<el-container>
			<!-- 顶部区域-->
			<el-header>
				<el-menu :default-active="activeIndex" class="el-menu" mode="horizontal" :ellipsis="false"
					:router="true">
					<div class="flex-grow" />
					<!-- 返回按钮 -->
					<el-menu-item index="/" class="min_hide">返回</el-menu-item>
					<!-- 企业账号顶部导航 -->
					<el-menu-item index="/" style="margin-left: 650px;">通知</el-menu-item>
					<el-menu-item index="/">面试</el-menu-item>
					<el-menu-item index="/">我的收藏</el-menu-item>
					<el-menu-item index="/">招聘数据</el-menu-item>
					<el-menu-item index="/">我的主页</el-menu-item>
					<el-menu-item index="/companyLogin"><el-button>企业登录</el-button></el-menu-item>
				</el-menu>
			</el-header>
			<!-- 中间区域 -->
			<el-main>
				<router-view></router-view>
			</el-main>
		</el-container>
	</el-container>
</template>

<script>
</script>

<style scoped>
	.el-container {
		height: 100%;
	}

	.el-aside {
		display: block;
		position: relative;
		background-color: #324157 !important;
	}

	header {
		border-bottom: solid 1px var(--el-menu-border-color);
		height: 45px !important;
		padding: 0 0 !important;
		background: white;
		position: fixed;
		z-index: 1000;
		width: 100%;
	}
</style>