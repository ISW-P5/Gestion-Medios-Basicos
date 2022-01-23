<template>
    <content-loading v-bind="$attrs" :width="width" :height="height">
        <template v-for="r in rows">
            <template v-for="c in columns">
                <rect :key="r + '_' + c" :x="getXPos(c)" :y="getYPos(r)" rx="3" ry="3" :width="getWidth()" :height="4" />
            </template>
            <rect :key="r + '_l'" v-if="r < rows" x="0" :y="getYPos(r) + 10" :width="width" :height="1" />
        </template>
    </content-loading>
</template>

<script>
import ContentLoading from "./ContentLoading";

export default {
    name: "TableLoading",
    components: {
        ContentLoading,
    },
    props: {
        header: {
            default: true,
            type: Boolean,
        },
        rows: {
            default: 5,
            type: Number,
        },
        columns: {
            default: 4,
            type: Number,
        },
    },
    computed: {
        height() {
            return (this.rows * 15) - 20;
        },
        width() {
            return ((this.columns - 1) * 20) + 10 + (this.columns * 85);
        },
    },
    methods: {
        getXPos(column) {
            return 5 + ((column - 1) * 100) + (column - 1);
        },
        getYPos(row) {
            return (row - 1) * 15;
        },
        getWidth() {
            return Math.random() * (90 - 80) + 80;
        }
    },
};
</script>
