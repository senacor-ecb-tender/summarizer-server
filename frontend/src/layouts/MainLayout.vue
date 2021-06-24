<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title class="ecb-font-bold">
          ECB Text Summarizer
        </q-toolbar-title>
        <q-space/>
        <div class="q-gutter-sm row items-center no-wrap ecb-font-regular">
          <q-btn push color="secondary" text-color="white" label="Summarize" icon="menu_book" v-if="$q.screen.gt.sm" @click="openDialog = true">
            <q-tooltip>Run summarization</q-tooltip>
          </q-btn>
          <q-space/>
          <q-avatar>
            <img src="../assets/logo_toolbar.jpg">
          </q-avatar>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-1"
    >
      <q-list>
        <q-item-label
          header
          class="text-grey-8 ecb-font-regular"
        >
          Menu
        </q-item-label>
        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-dialog v-model="openDialog" @hide="reset()" >
      <q-card style="width: 80%; max-width: 80%; height: 70%; max-height: 70%">
        <q-card-section horizontal>
          <q-card-section class="col-3">
            <div class="q-pa-md">
              <div class="row q-gutter-x-md q-gutter-y-md">
                <div class="col-grow q-gutter-x-md q-gutter-y-md">
                  <q-select
                    style="overflow: auto;"
                    filled
                    v-model="topicType"
                    :options="optionsTopic"
                    option-label="label"
                    option-value="id"
                    label="Type of topic">
                    <template v-slot:prepend>
                      <q-icon name="my_location"/>
                    </template>
                  </q-select>
                </div>
              </div>
              <div class="row q-gutter-x-md q-gutter-y-md">
                <div class="col-grow q-gutter-x-md q-gutter-y-md">
                  <q-select
                    style="overflow: auto;"
                    filled
                    v-model="summaryType"
                    :options="optionsSummary"
                    option-label="label"
                    option-value="id"
                    label="Size of summary">
                    <template v-slot:prepend>
                      <q-icon name="article"/>
                    </template>
                  </q-select>
                </div>
              </div>
              <div class="row q-gutter-x-md q-gutter-y-md justify-center items-center content-center">
                <div class="col q-gutter-x-md q-gutter-y-md justify-center items-center content-center">
                  <q-uploader
                    label="File to summarize"
                    :factory="factoryFn"
                    @uploaded="summarize"
                    @failed="failed"
                    @added="setFileSelected"
                    @removed="unsetFileSelected"
                    hide-upload-btn
                    color="white"
                    text-color="black"
                    flat
                    bordered
                    accept=".txt"
                    ref="uploader"
                  />
                </div>
              </div>
              <div class="row q-gutter-x-md q-gutter-y-md justify-center items-center content-center">
                <div class="col q-gutter-x-md q-gutter-y-md justify-center items-center content-center">
                  <q-btn :disabled="!isComplete" push color="primary" text-color="white" label="Summarize" icon="menu_book" @click="$refs.uploader.upload()">
                    <q-tooltip>Run summarization</q-tooltip>
                  </q-btn>
                  <q-btn push color="secondary" text-color="white" label="Reset" @click="reset()">
                    <q-tooltip>Reset</q-tooltip>
                  </q-btn>
                </div>
              </div>
            </div>
          </q-card-section>
          <q-separator/>
          <q-card-section v-if="summaryVisible" class="col-6">
            <div class="fit q-pa-md row">
              <q-card flat style="overflow: auto;">
                <q-card-section>
                  <div class="text-h6">Summary</div>
                </q-card-section>

                <q-separator dark inset/>

                <q-card-section>
                  {{ summarization }}
                </q-card-section>

              </q-card>
            </div>
          </q-card-section>
          <q-card-section v-if="summaryVisible">
            <div class="fit q-pa-md row">
              <q-card flat style="overflow: auto;">
                <q-card-section>
                  <div class="text-h6">Rate the summary</div>
                </q-card-section>

                <q-separator dark inset/>

                <q-card-section>
                  <q-rating
                    v-model="ratingModel"
                    size="2em"
                    color="primary"
                    icon="star_border"
                    icon-selected="star"
                  />
                </q-card-section>
                <q-card-section>
                  By rating the quality of the summary you can improve
                  the model quality by providing better training data
                  for future model tuning.
                  <br><br>
                  This feature is not implemented yet.
                </q-card-section>
              </q-card>
            </div>
          </q-card-section>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-page-container>
      <router-view/>
    </q-page-container>
  </q-layout>


</template>

<script>

import EssentialLink from 'components/EssentialLink.vue'
import {ref} from 'vue'
import { useQuasar } from 'quasar'

const linksData = [
  {
    title: 'Docs',
    caption: 'See documentation',
    icon: 'school',
    link: 'https://quasar.dev'
  },
  {
    title: 'Github',
    caption: 'See code repository',
    icon: 'code',
    link: 'https://github.com/senacor-ecb-tender'
  }
];

export default {
  name: 'MainLayout',
  components: {EssentialLink},
  data() {
    return {
      leftDrawerOpen: false,
      essentialLinks: linksData,
      optionsTopic: [
        {
          id: 'asset_quality',
          label: 'Asset Quality'
        },
        {
          id: 'climate_risk',
          label: 'Climate Risk'
        },
        {
          id: 'pandemic',
          label: 'Pandemic'
        },
        {
          id: 'credit_lending',
          label: 'Credit Lending'
        }
      ],
      optionsSummary: [
        {
          id: 'long',
          label: 'Long version'
        },
        {
          id: 'short',
          label: 'Short version'
        }
      ],
      topicType: "",
      summaryType: "",
      fileSelected: "",
      summarization: "...",
      openDialog: false,
      summaryVisible: false
    }
  },
  setup () {
    const $q = useQuasar()
    return {
      ratingModel: ref(0),
      failed(info) {
        $q.notify({
          type: 'negative',
          message: 'Call to Summarization API failed: Error code ' + info.xhr.status
        })
      }
    }
  },
  computed: {
    isComplete () {
      return this.topicType != "" && this.summaryType != "" && this.fileSelected != "";
    }
  },
  methods: {
    setFileSelected() {
      this.fileSelected = "true"
    },
    unsetFileSelected() {
      this.fileSelected = ""
    },
    reset() {
      this.summaryVisible = false
      this.summaryType = ""
      this.topicType = ""
      this.fileSelected = ""
      this.$refs.uploader.reset()
    },
    factoryFn (files) {
      return {
        url: 'http://20.93.176.254/upload',
        method: 'POST',
        fieldName: 'file',
        formFields: [{name: 'topic', value: this.topicType.id}, {name: 'summary_type', value: this.summaryType.id}]
      }
    },
    summarize ({ files, xhr }) {
      this.summarization = JSON.parse(xhr.response).result
      this.summaryVisible = true
    }
  }
}
</script>
