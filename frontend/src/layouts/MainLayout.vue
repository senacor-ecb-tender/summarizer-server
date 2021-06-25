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
          <q-btn flat push color="secondary" text-color="white" label="Summarize" icon="menu_book"
                 v-if="$q.screen.gt.sm" @click="openDialog = true">
            <q-tooltip>Run summarization</q-tooltip>
          </q-btn>
          <q-space/>
          <q-avatar>
            <img src="~assets/logo_toolbar.jpg">
          </q-avatar>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
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

    <q-dialog v-model="openDialog" @close="reset" @hide="reset" full-width full-height>
      <div class="row" style="overflow: auto; height: inherit;">
        <div class="col-3" style="background-color: white;">
          <q-card style="overflow: auto;" flat square>
            <q-card-section>
              <div class="text-h6 text-primary">Setup</div>
            </q-card-section>
            <q-card-section>
              <q-select
                style="overflow: auto;"
                outlined
                dense
                v-model="topicType"
                :options="optionsTopic"
                option-label="label"
                option-value="id"
                label="Type of topic">
                <template v-slot:prepend>
                  <q-icon name="my_location"/>
                </template>
              </q-select>
            </q-card-section>
            <q-card-section>
              <q-select
                style="overflow: auto;"
                outlined
                dense
                v-model="summaryType"
                :options="optionsSummary"
                option-label="label"
                option-value="id"
                label="Size of summary">
                <template v-slot:prepend>
                  <q-icon name="article"/>
                </template>
              </q-select>
            </q-card-section>
            <q-card-section>
              <q-uploader
                style="overflow: auto; width: inherit"
                label="Textfile"
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
            </q-card-section>
            <q-card-actions align="center">
              <q-btn unelevated :disabled="!isComplete" color="primary" label="Summarize"
                     @click="$refs.uploader.upload()">
                <q-tooltip>Run summarization</q-tooltip>
              </q-btn>
              <q-btn unelevated color="primary" label="Reset" @click="reset()">
                <q-tooltip>Reset</q-tooltip>
              </q-btn>
              <q-btn unelevated color="primary" label="Close" @click="close()">
                <q-tooltip>Close</q-tooltip>
              </q-btn>
            </q-card-actions>
          </q-card>
        </div>
        <q-separator vertical color="primary" size="0.15rem"/>

        <div v-if="summaryVisible" class="col-6" style="background-color: white">
          <q-card flat style="overflow: auto;" square>
            <q-card-section>
              <div class="text-h6 text-primary">Summary</div>
            </q-card-section>

            <q-card-actions>
              <q-btn flat round color="primary" icon="save" @click="exportSummary"/>
            </q-card-actions>
            <q-card-section>
              {{ summarization }}
            </q-card-section>
          </q-card>
        </div>

        <div v-if="summaryVisible" class="col-2" style="background-color: white">
          <q-card flat style="overflow: auto;" square>
            <q-card-section>
              <div class="text-h6 text-primary">Rating</div>
            </q-card-section>

            <q-card-section>
              <q-rating
                v-model="ratingModel"
                size="1.5em"
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
      </div>
    </q-dialog>

    <q-page-container>
      <router-view/>
    </q-page-container>
  </q-layout>


</template>

<script>

import EssentialLink from 'components/EssentialLink.vue'
import {ref} from 'vue'
import {exportFile, useQuasar} from 'quasar'

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
  setup() {
    const $q = useQuasar()
    return {
      ratingModel: ref(0),
      failed(info) {
        $q.notify({
          type: 'negative',
          message: 'Call to Summarization API failed!'
        })
      }
    }
  },
  computed: {
    isComplete() {
      return this.topicType != "" && this.summaryType != "" && this.fileSelected != "";
    }
  },
  methods: {
    exportSummary() {
      const $q = useQuasar()

      const status = exportFile('summary.txt', this.summarization, {
        encoding: 'UTF-8',
        mimeType: 'text/plain;charset=UTF-8;'
      })

      if (status === true) {
        // browser allowed it
      } else {
        // browser denied it
        $q.notify({
          type: 'negative',
          message: 'Browser does not allow the export: Error code ' + status
        })
      }
    },
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
    close() {
      this.openDialog = false
    },
    factoryFn(files) {
      return {
        url: process.env.API + '/upload',
        method: 'POST',
        fieldName: 'file',
        formFields: [{name: 'topic', value: this.topicType.id}, {name: 'summary_type', value: this.summaryType.id}]
      }
    },
    summarize({files, xhr}) {
      this.summarization = JSON.parse(xhr.response).result
      this.summaryVisible = true
    }
  }
}
</script>
